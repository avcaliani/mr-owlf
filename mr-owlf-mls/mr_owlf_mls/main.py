import pickle
from logging import getLogger
from os import environ as env

from pandas import DataFrame
from pymongo import MongoClient
from pymongo.database import Database
from repository.post import PostRepository
from service.ml import modeling
from util import ai
from util import database
from util.log import init

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'

DB_NAME = env.get('APP_DB_NAME', 'mr-owlf-db')
CLF_FILE = env.get('APP_CLF_FILE', './classifier.pkl')
VECTORIZER_FILE = env.get('APP_VECTORIZER_FILE', './vectorizer.pkl')

init()
log = getLogger('root')


def save(obj: any, file: str) -> None:
    log.info(f'Saving file "{file}"')
    _file = open(file, 'wb')
    pickle.dump(obj=obj, file=_file, protocol=-1)
    _file.close()


def run(db: Database) -> None:
    repository = PostRepository(db)
    log.info(f'DB # "{repository.count()}" records found!\n')
    df: DataFrame = repository.find()

    cvec_df: DataFrame = ai.count_vectorizer(df)
    unigrams = list(ai.unigrams(cvec_df))

    cvec_df: DataFrame = ai.count_vectorizer(df, ngram_range=(2, 2))
    bigrams = list(ai.unigrams(cvec_df))

    stop_words = ai.get_stop_words(unigrams, bigrams)

    clf, vectorizer = modeling.get_model(df, stop_words)
    save(clf, CLF_FILE)
    save(vectorizer, VECTORIZER_FILE)


if __name__ == '__main__':
    log.info('Starting Mr. Owlf: Data Stream Service...')
    client: MongoClient = database.connect()
    try:
        run(client[DB_NAME])
    except Exception as ex:
        log.fatal(f'Application has been interrupted!\n{ex}')
    finally:
        database.disconnect(client)
        log.info('See ya!')

from logging import getLogger
from os import environ as env

from pandas import DataFrame
from pymongo import MongoClient
from pymongo.database import Database

from repository.post import PostRepository
from service import modeling
from service.process import Process
from util import ai
from util import database
from util.log import init

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'

DB_NAME = env.get('MR_OWLF_DB_NAME', 'mr-owlf-db')

init()
log = getLogger('root')


def run(db: Database) -> None:

    repository = PostRepository(db)

    log.info(f'"{repository.count()}" records found!\n')
    df: DataFrame = repository.find()

    cvec_df: DataFrame = ai.count_vectorizer(df)
    unigrams = list(ai.unigrams(cvec_df))

    cvec_df: DataFrame = ai.count_vectorizer(df, ngram_range=(2, 2))
    bigrams = list(ai.unigrams(cvec_df))

    stop_words = ai.get_stop_words(unigrams, bigrams)

    clf, vectorizer = modeling.get_model(df, stop_words)

    # FIXME: Remove it
    sentences = [
        'San Diego backyard shed rents for $1,050 a month',
        'Are You The Whistleblower? Trump Boys Ask White House Janitor After Giving Him Serum Of All The Sodas Mixed Together',
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean at diam ac orci pharetra scelerisque non sit amet turpis. Donec quis erat quam',
        '12356487984158641351568463213851684132168461'
    ]

    process = Process(clf, vectorizer, db)
    for sentence in sentences:
        process.run(
            sentence=sentence,
            author='avcaliani',
            domain='github.com'
            # publish_date=
        )


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

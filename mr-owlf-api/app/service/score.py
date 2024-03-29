import pickle
from logging import getLogger
from os import environ as env
from os import path

from mr_owlf_mls.service.process import Process
from pymongo import MongoClient

from service import database

DB_NAME = env.get('APP_DB_NAME', 'mr-owlf-db')
CLF_FILE = env.get('APP_CLF_FILE', '../tmp/classifier.pkl')
VECTORIZER_FILE = env.get('APP_VECTORIZER_FILE', '../tmp/vectorizer.pkl')
log = getLogger('root')


def is_ready() -> bool:
    clf = path.exists(CLF_FILE)
    vectorizer = path.exists(VECTORIZER_FILE)
    log.info(f'File Status: CLF "{clf}" / VECTORIZER "{vectorizer}"')
    return clf and vectorizer


def get_score(data: any) -> any:
    """
    Calculate data score.
    :param data: Data to be processed
    :return: Score
    """
    conn: MongoClient = database.connect()
    process = Process(load(CLF_FILE), load(VECTORIZER_FILE), conn[DB_NAME])
    score = process.run(
        sentence=data['sentence'] if 'sentence' in data else None,
        author=data['author'] if 'author' in data else None,
        domain=data['domain'] if 'domain' in data else None,
        publish_date=data['publish_date'] if 'publish_date' in data else None
    )
    database.disconnect(conn)
    return {
        'score': float('{0:.2f}'.format(score, 2)),
        'status': get_status(score)
    }


def get_status(score: float) -> str:
    if score < 0.5:
        return 'FAKE'
    elif score < 0.7:
        return 'MAYBE_FAKE'
    elif score < 0.9:
        return 'MAYBE_NOT_FAKE'
    else:
        return 'NOT_FAKE'


def load(file: str) -> any:
    _file = open(file, 'rb')
    obj = pickle.load(_file)
    _file.close()
    return obj

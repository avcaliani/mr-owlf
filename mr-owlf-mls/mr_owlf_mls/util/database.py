from logging import getLogger
from os import environ as env
from sys import exc_info
from time import sleep

from pandas import DataFrame
from cassandra.cluster import Cluster, Session

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'

LOG_NAME = 'root'
DB_CONN = env.get('MR_OWLF_DB_CONN', '0.0.0.0')
DB_PORT = env.get('MR_OWLF_DB_PORT', '9042')
DB_KEYSPACE = env.get('MR_OWLF_DB_KEYSPACE', 'mr_owlf_ks')


def connect(retry: bool = True) -> Session:
    log = getLogger(LOG_NAME)
    log.info(f'DB Info -> [Host: "{DB_CONN}"] [Port: "{DB_PORT}"] [Key Space: "{DB_KEYSPACE}"]')
    while retry:
        try:
            session = Cluster([DB_CONN], port=int(DB_PORT)).connect(DB_KEYSPACE, wait_for_all_pools=True)
            session.row_factory = __pandas_factory
            log.info('Successfully connected to database!')
            return session
        except:
            log.warning('Error while connecting to database. Trying again in a few moments...')
            log.debug(f'Error Class: {exc_info()[0]}')
            sleep(5)
    return None


def disconnect(session: Session) -> None:
    log = getLogger(LOG_NAME)
    try:
        if session is not None:
            session.cluster.shutdown()
            log.info('Successfully disconnected from database!')
    except:
        log.warning('Error while shutting down database connection.')
        log.debug(f'Error Class: {exc_info()[0]}')


def __pandas_factory(cols: list, rows: list) -> DataFrame:
    return DataFrame(rows, columns=cols)

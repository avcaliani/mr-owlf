from logging import getLogger
from os import environ as env
from sys import exc_info
from time import sleep

from pymongo import MongoClient

LOG_NAME = 'root'
DB_CONN = env.get('APP_DB_CONN', 'localhost')
DB_PORT = env.get('APP_DB_PORT', '27017')
DB_NAME = env.get('APP_DB_NAME', 'mr-owlf-db')
DB_USER = env.get('APP_DB_USER', 'api')
DB_PASSWORD = env.get('APP_DB_PASSWORD', '4P1')


def connect(retry: bool = True) -> MongoClient:
    log = getLogger(LOG_NAME)
    log.info(f'DB Info -> [Host: "{DB_CONN}"] [Port: "{DB_PORT}"] [DB Name: "{DB_NAME}"]')
    while retry:
        try:
            client = MongoClient(f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_CONN}:{DB_PORT}/{DB_NAME}")
            log.info('Successfully connected to database!')
            return client
        except:
            log.warning('Error while connecting to database. Trying again in a few moments...')
            log.debug(f'Error Class: {exc_info()[0]}')
            sleep(5)
    return None


def disconnect(client: MongoClient) -> None:
    log = getLogger(LOG_NAME)
    try:
        if client is not None:
            client.close()
            log.info('Successfully disconnected from database!')
    except:
        log.warning('Error while shutting down database connection.')
        log.debug(f'Error Class: {exc_info()[0]}')

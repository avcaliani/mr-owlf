from logging import getLogger
from os import environ as env

from pandas import DataFrame
from pymongo import MongoClient
from pymongo.database import Database

from repository.post import PostRepository
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
    log.info(f'"{repository.count()}" records found!')
    posts: DataFrame = repository.find()
    print(posts.head(5))
    print(posts.tail(5))


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

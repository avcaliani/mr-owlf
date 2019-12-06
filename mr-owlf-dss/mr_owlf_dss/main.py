from logging import getLogger
from os import environ as env

from ingestor.reddit import Reddit
from pandas import DataFrame
from pymongo import MongoClient
from pymongo.database import Database
from repository.post_repository import PostRepository
from util import database as db
from util.log import init

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'

DB_NAME = env.get('MR_OWLF_DB_NAME', 'mr-owlf-db')

init()
log = getLogger('root')


def run(conn: Database) -> None:
    posts: DataFrame = Reddit().exec()
    post_repository = PostRepository(conn)
    post_repository.add(posts)
    log.info(f'Current Posts -> "{post_repository.count()}"')


if __name__ == '__main__':
    log.info('Starting Mr. Owlf: Data Stream Service...')
    client: MongoClient = db.connect()
    try:
        run(client[DB_NAME])
    except Exception as ex:
        log.fatal(f'Application has been interrupted!\n{ex}')
    finally:
        db.disconnect(client)
        log.info('See ya!')

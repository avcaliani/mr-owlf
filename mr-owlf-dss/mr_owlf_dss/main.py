from logging import getLogger
from os import environ as env

import ingestor.reddit as reddit
import service.statistics as statistics
from pandas import DataFrame
from pymongo import MongoClient
from pymongo.database import Database
from repository.author import AuthorRepository
from repository.post import PostRepository
from util import database as db
from util.log import init

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'

DB_NAME = env.get('APP_DB_NAME', 'mr-owlf-db')

init()
log = getLogger('root')


def run(conn: Database) -> None:
    post_repository = PostRepository(conn)
    author_repository = AuthorRepository(conn)

    log.info(f'Starting "Reddit" data processing..."')
    posts: DataFrame = reddit.run()
    for index, post in posts.iterrows():
        post_repository.add(post)
        statistics.author(author_repository, post)

    log.info(f'Current Posts   -> "{post_repository.count()}"')
    log.info(f'Current Authors -> "{author_repository.count()}"')


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

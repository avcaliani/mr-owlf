from logging import getLogger
from os import environ as env
from pprint import pformat

import ingestor.reddit as reddit
import service.statistics as statistics
from pandas import DataFrame
from pymongo import MongoClient
from pymongo.database import Database
from repository.author import AuthorRepository
from repository.domain import DomainRepository
from repository.post import PostRepository
from repository.statistic import StatisticRepository
from util import database
from util.log import init

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'

DB_NAME = env.get('APP_DB_NAME', 'mr-owlf-db')

init()
log = getLogger('root')


def run(db: Database) -> None:
    post_repository = PostRepository(db)
    author_repository = AuthorRepository(db)
    domain_repository = DomainRepository(db)
    statistic_repository = StatisticRepository(db)

    log.info(f'Starting "Reddit" data processing..."')
    posts: DataFrame = reddit.run()
    for index, post in posts.iterrows():
        post_repository.add(post)
        statistics.author(author_repository, post)
        statistics.domain(domain_repository, post)

    log.info(f'Posts   -> "{post_repository.count()}"')
    log.info(f'Authors -> "{author_repository.count()}"')
    log.info(f'Domains -> "{domain_repository.count()}"')

    log.info(f'Calculating statistics...')
    result: dict = statistics.general(statistic_repository, post_repository.find())
    log.info(f'Result...\n{pformat(result)}')


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

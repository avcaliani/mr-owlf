from logging import getLogger

from cassandra.cluster import Session
from ingestor.reddit import Reddit
from pandas import DataFrame
from repository.post_repository import PostRepository
from util import database as db
from util.log import init

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'

init()
log = getLogger('root')


def run(conn: Session) -> None:
    posts: DataFrame = Reddit().exec()
    post_repository = PostRepository(conn)
    post_repository.add(posts)
    log.info(f'Current Posts -> "{post_repository.count()}"')


if __name__ == '__main__':
    log.info('Starting Mr. Owlf: Data Stream Service...')
    _conn: Session = db.connect()
    try:
        run(_conn)
    except Exception as ex:
        log.fatal(f'Application has been interrupted!\n{ex}')
    finally:
        db.disconnect(_conn)
        log.info('See ya!')

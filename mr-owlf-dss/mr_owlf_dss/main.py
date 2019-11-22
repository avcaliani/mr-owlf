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
    print(f'{posts.head(2)}\n...\n{posts.tail(2)}\n{posts.shape}')

    PostRepository(conn).add(posts)

    # log.info(f'Posts: {conn.execute("SELECT COUNT(*) FROM posts").one()[0]}')
    # log.info(f'Inserting new post...')
    # conn.execute(
    #     "INSERT INTO posts (author, title, content) VALUES (%s, %s, %s)",
    #     ('dss', 'Post X', 'Content 0X')
    # )
    #
    # log.info(f'(Updated) Posts: {conn.execute("SELECT COUNT(*) FROM posts").one()[0]}')
    # rows = conn.execute('SELECT * FROM posts')
    # for row in rows:
    #     print(row.author, row.title, row.content)


if __name__ == "__main__":
    log.info('Starting Mr. Owlf: Data Stream Service...')
    _conn: Session = db.connect()
    try:
        run(_conn)
    except:
        log.fatal("Application has been interrupted!")
    finally:
        db.disconnect(_conn)
        log.info("See ya!")

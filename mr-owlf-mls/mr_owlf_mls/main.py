from os import environ as env
from _pickle import dump
from logging import getLogger
from mongodb.cluster import Cluster

from cassandra.cluster import Session
from pandas import DataFrame
from service.nlp_service import NLPService
from util import database as db
from util.log import init

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'

CLF_FILE = env.get('MR_OWLF_CLF_FILE', '../.shared/clf.pkl')

init()
log = getLogger('root')


def run(conn: Session) -> None:
    log.info(f'Current Posts -> "{conn.execute("SELECT COUNT(*) FROM posts")}"')
    rows = conn.execute('SELECT * FROM posts')
    posts: DataFrame = rows._current_rows
    print(posts.head())
    _results = []
    for index, post in posts.iterrows():
        _results.append({
            'author': post.author, 'title': post.title
        })
        log.info(f'{post.author}, {post.title}')

    out_file = open(CLF_FILE, 'wb')
    dump(list(_results), out_file, -1)
    out_file.close()
    NLPService().exec(posts)


if __name__ == '__main__':
    log.info('Starting Mr. Owlf: Machine Learning Service...')
    _conn: Session = db.connect()
    # try:
    run(_conn)
    # except Exception as ex:
    #     log.fatal(f'Application has been interrupted!\n{ex}')
    # finally:
    #     db.disconnect(_conn)
    #     log.info('See ya!')

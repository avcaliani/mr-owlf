from os import environ as env
from _pickle import dump
from logging import getLogger
from cassandra.cluster import Cluster
from util.log import init

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'

DB_CONN = env.get('MR_OWLF_DB_CONN', '0.0.0.0')
DB_PORT = env.get('MR_OWLF_DB_PORT', '9042')
DB_KEYSPACE = env.get('MR_OWLF_DB_KEYSPACE', 'mr_owlf_ks')
CLF_FILE = env.get('MR_OWLF_CLF_FILE', '../../.shared/clf.pkl')

init()  # Initializing Logger
log = getLogger('root')

log.info("""
        __________
       / ___  ___ \\
      / / @ \/ @ \ \\
      \ \___/\___/ /\\
       \____\/____/||
       /     /\\\\\\\\\\//
       |     |\\\\\\\\\\\\
        \      \\\\\\\\\\\\
         \______/\\\\\\\\
          _||_||_
           -- --
          Mr. Owlf
> Machine Learning Service <
""")


def run():
    log.info(f'Connecting to our cluster...')
    cluster = Cluster([DB_CONN], port=int(DB_PORT))
    session = cluster.connect(DB_KEYSPACE, wait_for_all_pools=True)

    log.info(f'Posts: {session.execute("SELECT COUNT(*) FROM posts").one()[0]}')
    rows = session.execute('SELECT * FROM posts')
    _results = []
    for row in rows:
        _results.append({
            'author': row.author, 'title': row.title, 'author': row.content
        })
        log.info(f'{row.author}, {row.title}, {row.content}')

    out_file = open(CLF_FILE, 'wb')
    dump(list(_results), out_file, -1)
    out_file.close()


if __name__ == "__main__":
    log.info(f"""
Environment
----------------------------------------
MR_OWLF_DB_CONN     '{DB_CONN}'
MR_OWLF_DB_PORT     '{DB_PORT}'
MR_OWLF_DB_NAME     '{DB_KEYSPACE}'
MR_OWLF_CLF_FILE    '{CLF_FILE}'
    """)
    run()
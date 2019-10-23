from os import environ as env
from logging import getLogger
from cassandra.cluster import Cluster
from util.log import init

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'

DB_CONN = env.get('MR_OWLF_DB_CONN', '0.0.0.0')
DB_PORT = env.get('MR_OWLF_DB_PORT', '9042')
DB_KEYSPACE = env.get('MR_OWLF_DB_KEYSPACE', 'mr_owlf_ks')

print("""
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
 > Data Stream Service <
""")


def run():
    log.info(f'Connecting to our cluster...')
    cluster = Cluster([DB_CONN], port=int(DB_PORT))
    session = cluster.connect(DB_KEYSPACE, wait_for_all_pools=True)

    log.info(f'Posts: {session.execute("SELECT COUNT(*) FROM posts").one()[0]}')
    log.info(f'Inserting new post...')
    session.execute(
        "INSERT INTO posts (author, title, content) VALUES (%s, %s, %s)",
        ('dss', 'Post X', 'Content 0X')
    )

    log.info(f'(Updated) Posts: {session.execute("SELECT COUNT(*) FROM posts").one()[0]}')
    rows = session.execute('SELECT * FROM posts')
    for row in rows:
        print(row.author, row.title, row.content)


if __name__ == "__main__":
    init()  # Initializing Logger
    log = getLogger('root')
    log.info(f"""
Environment
----------------------------------------
MR_OWLF_DB_CONN     '{DB_CONN}'
MR_OWLF_DB_PORT     '{DB_PORT}'
MR_OWLF_DB_NAME     '{DB_KEYSPACE}'
    """)
    run()

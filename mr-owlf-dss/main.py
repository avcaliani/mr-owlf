from os import environ as env
from pymongo import MongoClient

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'


DB_CONN = env.get('MR_OWLF_DB_CONN', 'localhost')
DB_PORT = env.get('MR_OWLF_DB_PORT', '27017')
DB_NAME = env.get('MR_OWLF_DB_NAME', 'mr-owlf-db')
DB_USER = env.get('MR_OWLF_DB_USER', 'dss')
DB_PASSWORD = env.get('MR_OWLF_DB_PASSWORD', 'D4t4SS')

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
 > Data Sream Service <
""")


def run():
    client = MongoClient(f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_CONN}:{DB_PORT}/{DB_NAME}")
    db = client['mr-owlf-db']
    posts = db['posts']
    result = posts.insert_one({
        'title': 'Python and MongoDB',
        'content': 'PyMongo is fun, you guys',
        'author': 'Scott'
    })
    print('One post: {0}'.format(result.inserted_id))
    # posts.drop()
    client.close()
    pass


if __name__ == "__main__":
    print(f"""
Environment
----------------------------------------
MR_OWLF_DB_CONN     '{DB_CONN}'
MR_OWLF_DB_PORT     '{DB_PORT}'
MR_OWLF_DB_NAME     '{DB_NAME}'
MR_OWLF_DB_USER     '{DB_USER}'
MR_OWLF_DB_PASSWORD '{DB_PASSWORD}'
    """)
    run()
else:
    print("I'm sorry, but I can't be used as a lib :/")

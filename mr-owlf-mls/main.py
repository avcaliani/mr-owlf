from os import environ as env
from _pickle import dump
from pymongo import MongoClient

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'


DB_CONN = env.get('MR_OWLF_DB_CONN', 'localhost')
DB_PORT = env.get('MR_OWLF_DB_PORT', '27017')
DB_NAME = env.get('MR_OWLF_DB_NAME', 'mr-owlf-db')
DB_USER = env.get('MR_OWLF_DB_USER', 'mls')
DB_PASSWORD = env.get('MR_OWLF_DB_PASSWORD', 'ML34rn')
CLF_FILE = env.get('MR_OWLF_CLF_FILE', './clf.pkl')

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
> Machine Learning Service <
""")


def run():
    client = MongoClient(f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_CONN}:{DB_PORT}/{DB_NAME}")
    db = client['mr-owlf-db']
    posts = db['posts']

    results = posts.find()
    _results = []
    for post in results:
        post['_id'] = str(post['_id'])
        _results.append(post)
        print(f'* {post}')

    out_file = open(CLF_FILE, 'wb')
    dump(list(_results), out_file, -1)

    out_file.close()
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
MR_OWLF_CLF_FILE    '{CLF_FILE}'
    """)
    run()
else:
    print("I'm sorry, but I can't be used as a lib :/")

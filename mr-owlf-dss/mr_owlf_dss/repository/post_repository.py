from logging import getLogger

from pandas import DataFrame
from pymongo.collection import Collection
from pymongo.database import Database

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'


class PostRepository:

    def __init__(self, db: Database):
        self.log = getLogger('root')
        self.db = db

    def add(self, posts: DataFrame) -> None:

        dao: Collection = self.db['posts']
        for index, post in posts.iterrows():
            result = dao.insert_one({
                "author"        : post.author,
                "title"         : post.title,
                "timestamp"     : post.timestamp,
                "domain"        : post.domain,
                "classification": str(post.__classification__)
            })
            self.log.debug('Inserted post: {0}'.format(result.inserted_id))

        self.log.info(f'{posts.shape[0]} posts processed \\o/')

    def count(self) -> int:
        return self.db['posts'].count_documents({})

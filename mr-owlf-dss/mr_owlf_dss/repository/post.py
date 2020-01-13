from logging import getLogger

from pandas import DataFrame
from pymongo.collection import Collection
from pymongo.database import Database


class PostRepository:

    def __init__(self, db: Database):
        self.log = getLogger('root')
        self.db = db

    def add(self, posts: DataFrame) -> None:
        dao: Collection = self.db['posts']
        for index, post in posts.iterrows():
            result = dao.insert_one({
                'author': post.author,
                'content': post.content,
                'content_original': post.content_original,
                'timestamp': post.timestamp,
                'domain': post.domain,
                'classification': post.classification
            })
            self.log.debug('Inserted post: {0}'.format(result.inserted_id))

        self.log.info(f'{posts.shape[0]} posts processed \\o/')

    def count(self) -> int:
        return self.db['posts'].count_documents({})

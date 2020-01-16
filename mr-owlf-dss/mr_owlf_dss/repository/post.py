from logging import getLogger

from pandas import DataFrame
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database
from pymongo.results import InsertOneResult


class PostRepository:

    def __init__(self, db: Database):
        self.log = getLogger('root')
        self.collection: Collection = db['posts']

    def find(self) -> DataFrame:
        cursor: Cursor = self.collection.find({})
        return DataFrame(list(cursor))

    def add(self, post: any) -> None:
        result: InsertOneResult = self.collection.insert_one({
            'author': post.author,
            'content': post.content,
            'content_original': post.content_original,
            'timestamp': post.timestamp,
            'domain': post.domain,
            'classification': post.classification
        })
        self.log.debug('Inserted post: {0}'.format(result.inserted_id))

    def count(self) -> int:
        return self.collection.count_documents({})

from logging import getLogger

from pandas import DataFrame
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database


class PostRepository:

    def __init__(self, db: Database):
        self.log = getLogger('root')
        self.collection: Collection = db['posts']

    def find(self) -> DataFrame:
        cursor: Cursor = self.collection.find({})
        return DataFrame(list(cursor))

    def count(self) -> int:
        return self.collection.count_documents({})

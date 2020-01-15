from logging import getLogger

from bson.objectid import ObjectId
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertOneResult, UpdateResult


class AuthorRepository:

    def __init__(self, db: Database):
        self.log = getLogger('root')
        self.collection: Collection = db['authors']

    def find(self, name: str) -> any:
        return self.collection.find_one({'author': name})

    def add(self, name: any, classification: str) -> None:
        result: InsertOneResult = self.collection.insert_one({
            'author': name,
            'classification': {classification: 1}
        })
        self.log.debug('Inserted author: {0}'.format(result.inserted_id))

    def update(self, _id: ObjectId, classification: str, count: int) -> None:
        result: UpdateResult = self.collection.update_one(
            {'_id': _id}, {"$set": {f"classification.{classification}": count}}
        )
        self.log.debug('Updated authors: {0}'.format(result.modified_count))

    def count(self) -> int:
        return self.collection.count_documents({})

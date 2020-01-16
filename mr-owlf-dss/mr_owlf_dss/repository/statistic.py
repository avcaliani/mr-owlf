from logging import getLogger

from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertOneResult


class StatisticRepository:

    def __init__(self, db: Database):
        self.log = getLogger('root')
        self.collection: Collection = db['statistics']

    def add(self, data: any) -> None:
        result: InsertOneResult = self.collection.insert_one(data)
        self.log.debug('Inserted statistic: {0}'.format(result.inserted_id))

from logging import getLogger

from pymongo.collection import Collection
from pymongo.database import Database

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'


class DomainRepository:

    def __init__(self, db: Database):
        self.log = getLogger('root')
        self.db = db

    def find(self, name: str) -> any:
        dao: Collection = self.db['domains']
        domain: dict = dao.find_one({'domain': name})
        if domain is None:
            self.log.warning(f'Record not found for "{name}" domain :/')
        else:
            self.log.info(f'Record found for domain "{name}":\n"{domain}"')
        return domain

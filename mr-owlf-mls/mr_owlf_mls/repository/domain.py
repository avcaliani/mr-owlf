from logging import getLogger

from pymongo.collection import Collection
from pymongo.database import Database


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
            self.log.debug(f'Record found for domain "{name}": "{domain}"')
        return domain

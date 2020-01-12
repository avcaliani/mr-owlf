from logging import getLogger

from pymongo.collection import Collection
from pymongo.database import Database

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'


class AuthorRepository:

    def __init__(self, db: Database):
        self.log = getLogger('root')
        self.db = db

    def find(self, name: str) -> any:
        dao: Collection = self.db['authors']
        author: dict = dao.find_one({'author': name})
        if author is None:
            self.log.warning(f'Record not found for "{name}" author :/')
        else:
            self.log.debug(f'Record found for author "{name}": "{author}"')
        return author

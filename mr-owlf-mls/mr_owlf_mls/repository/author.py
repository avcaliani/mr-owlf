from logging import getLogger

from pymongo.collection import Collection
from pymongo.database import Database


class AuthorRepository:

    def __init__(self, db: Database):
        self.log = getLogger('root')
        self.collection: Collection = db['authors']

    def find(self, name: str) -> any:
        author: dict = self.collection.find_one({'author': name})
        if author is None:
            self.log.warning(f'Record not found for "{name}" author :/')
        else:
            self.log.debug(f'Record found for author "{name}": "{author}"')
        return author

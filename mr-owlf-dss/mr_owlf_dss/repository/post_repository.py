from logging import getLogger

from cassandra.cluster import Session
from pandas import DataFrame

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'


class PostRepository:

    def __init__(self, conn: Session):
        self.log = getLogger('root')
        self.conn = conn

    def add(self, posts: DataFrame) -> None:
        pass

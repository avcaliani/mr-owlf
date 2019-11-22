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

        query = self.conn.prepare(
            "INSERT INTO posts (author, title, last_update, classification, domain) VALUES (?, ?, ?, ?, ?)"
        )
        for index, post in posts.iterrows():
            self.conn.execute(query, (
                post.author,
                post.title,
                post.timestamp,
                post.domain,
                str(post.__classification__)
            ))
        self.log.info(f'{posts.shape[0]} posts processed \\o/')

    def count(self) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM posts").one()[0]

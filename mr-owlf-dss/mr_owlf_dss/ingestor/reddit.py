from logging import getLogger
from os import path, getcwd

from pandas import DataFrame, read_csv, concat

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'

DATA_DIR = path.realpath(path.join(getcwd(), path.dirname(__file__), '../../data/reddit'))


class Reddit:

    def __init__(self):
        self.log = getLogger('root')
        self.log.debug(f'Data Directory: "{DATA_DIR}"')

    def clean_data(self, posts: DataFrame) -> None:
        self.log.debug(f'Data Shape (Raw): {posts.shape}')
        posts.drop_duplicates(subset='title', inplace=True)             # Drop duplicate rows
        posts['title'] = posts['title'].str.replace('[^\w\s]', ' ')     # Remove punctuation
        posts['title'] = posts['title'].str.replace('[^A-Za-z]', ' ')   # Remove numbers
        posts['title'] = posts['title'].str.replace('\s{2,}', ' ')      # Make sure any double-spaces are single
        posts['title'] = posts['title'].str.lower()                     # Transform all text to lowercase
        posts.dropna(inplace=True)                                      # Remove null records
        self.log.debug(f'Data Shape (Cleaned): {posts.shape}')

    def exec(self) -> DataFrame:

        df_onion: DataFrame = read_csv(f'{DATA_DIR}/the-onion.csv')
        self.log.info(f'The Onion (Shape): {df_onion.shape}')

        df_not_onion: DataFrame = read_csv(f'{DATA_DIR}/not-the-onion.csv')
        self.log.info(f'Not The Onion (Shape): {df_not_onion.shape}')

        posts: DataFrame = concat([df_onion, df_not_onion], axis=0)
        self.log.info(f'Combined Shape: {posts.shape}')

        posts = posts.reset_index(drop=True)
        posts = posts.drop(columns=['n', 'num_comments', 'score'])
        self.clean_data(posts)

        # FIXME: POC Purpose
        posts["subreddit"] = posts["subreddit"].map({"nottheonion": 0, "TheOnion": 1})
        posts = posts.rename(columns={'subreddit': '__classification__'})

        return posts

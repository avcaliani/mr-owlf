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
        posts.drop_duplicates(subset='title', inplace=True)  # Drop duplicate rows
        posts['title'] = posts['title'].str.replace('[^\w\s]', ' ')  # Remove punctuation
        posts['title'] = posts['title'].str.replace('[^A-Za-z]', ' ')  # Remove numbers
        posts['title'] = posts['title'].str.replace('\s{2,}', ' ')  # Make sure any double-spaces are single
        posts['title'] = posts['title'].str.lower()  # Transform all text to lowercase
        posts.fillna("", inplace=True)  # Remove null values records

    def exec(self) -> DataFrame:
        df_onion: DataFrame = read_csv(f'{DATA_DIR}/the-onion.csv')
        self.log.info(f'Reddit: The Onion Posts     -> "{df_onion.shape[0]}"')

        df_not_onion: DataFrame = read_csv(f'{DATA_DIR}/not-the-onion.csv')
        self.log.info(f'Reddit: Not The Onion Posts -> "{df_not_onion.shape[0]}"')

        posts: DataFrame = concat([df_onion, df_not_onion], axis=0)
        self.log.info(f'Reddit: All Posts           -> "{posts.shape[0]}"')

        posts = posts.reset_index(drop=True)
        posts = posts.drop(columns=['n', 'num_comments', 'score'])
        self.clean_data(posts)

        # FIXME: POC Purpose
        posts["subreddit"] = posts["subreddit"].map({"nottheonion": 0, "TheOnion": 1})
        posts = posts.rename(columns={'subreddit': '__classification__'})

        self.log.info(f'Reddit: All Posts (Cleaned) -> "{posts.shape[0]}"')
        return posts

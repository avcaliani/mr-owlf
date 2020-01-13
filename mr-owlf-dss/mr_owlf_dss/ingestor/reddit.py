from logging import getLogger
from os import path, getcwd

from pandas import DataFrame, read_csv, concat

DATA_DIR = path.realpath(path.join(getcwd(), path.dirname(__file__), '../../data/reddit'))
log = getLogger('root')


def clean_data(posts: DataFrame) -> None:
    # Drop duplicate rows
    posts.drop_duplicates(subset='content', inplace=True)
    # Remove punctuation, numbers and duplicated spaces
    posts['content'] = posts['content'].str.replace('[^\w\s]', ' ')
    posts['content'] = posts['content'].str.replace('[^A-Za-z]', ' ')
    posts['content'] = posts['content'].str.replace('\s{2,}', ' ')
    # Transform all text to lowercase
    posts['content'] = posts['content'].str.lower()
    posts['author'] = posts['author'].str.lower()
    posts['domain'] = posts['domain'].str.lower()
    posts.fillna('', inplace=True)  # Remove null values records


def run() -> DataFrame:
    log.debug(f'Data Directory: "{DATA_DIR}"')
    df_onion: DataFrame = read_csv(f'{DATA_DIR}/the-onion.csv')
    log.info(f'Reddit: The Onion Posts     -> "{df_onion.shape[0]}"')

    df_not_onion: DataFrame = read_csv(f'{DATA_DIR}/not-the-onion.csv')
    log.info(f'Reddit: Not The Onion Posts -> "{df_not_onion.shape[0]}"')

    posts: DataFrame = concat([df_onion, df_not_onion], axis=0)
    log.info(f'Reddit: All Posts           -> "{posts.shape[0]}"')

    posts = posts.reset_index(drop=True)

    # Normalizing Classes
    posts['subreddit'] = posts['subreddit'].map({
        'nottheonion': 'FAKE',
        'TheOnion': 'NOT_FAKE'
    })

    # Updating Columns
    posts = posts.drop(columns=['n', 'num_comments', 'score'])
    posts = posts.rename(columns={
        'subreddit': 'classification',
        'title': 'content'
    })
    posts['content_original'] = posts['content']

    clean_data(posts)
    log.info(f'Reddit: All Posts (Cleaned) -> "{posts.shape[0]}"')
    return posts

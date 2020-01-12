from logging import getLogger
from typing import Tuple, List, Set

from nltk import download
from nltk.corpus import stopwords
from pandas import DataFrame, Series
from sklearn.feature_extraction.text import CountVectorizer

log = getLogger('root')


def count_vectorizer(df: DataFrame, ngram_range: Tuple[int, int] = (1, 1)) -> DataFrame:
    log.debug(f'COUNT VECTORIZER # [{ngram_range}]')
    cv = CountVectorizer(stop_words='english', ngram_range=ngram_range)
    df_cvec = DataFrame(
        cv.fit_transform(df['title']).toarray(),
        columns=cv.get_feature_names()
    )
    log.debug(f'COUNT VECTORIZER # Result Shape: {df_cvec.shape}\n')
    return df_cvec


def unigrams(df: DataFrame, n_exp: int = 10) -> Set:
    # Set up variables to contain top `n_exp` most used words
    log.debug(f'UNIGRAMS # Top {n_exp} expressions')

    top_exp: Series = df\
        .sum(axis=0)\
        .sort_values(ascending=False)\
        .head(n_exp)

    unigrams = set(top_exp.index)
    log.debug(f'UNIGRAMS # Result: {unigrams}\n')
    return unigrams


def get_stop_words(unigrams: List, bigrams: List) -> List:
    log.debug(f'STOP WORDS # Collecting...')
    download('stopwords')
    custom = list(stopwords.words('english'))

    for i in unigrams:
        custom.append(i)

    for i in bigrams:
        split_words = i.split(" ")
        for word in split_words:
            custom.append(word)

    log.debug(f'STOP WORDS # Result: {len(custom)}\n')
    return custom

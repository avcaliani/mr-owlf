from typing import Tuple
from pandas import DataFrame, Series, to_datetime, read_csv
from sklearn.feature_extraction.text import CountVectorizer
from nltk import download
from nltk.corpus import stopwords


def count_vectorizer(df: DataFrame, filter_value: int, ngram_range: Tuple[int, int] = (1, 1)) -> DataFrame:

    print(r'+-----------------------------------+')
    print(r'|         Count Vectorizer          |')
    print(r'+-----------------------------------+')

    # Set variables to show only one category titles
    titles = df[df['subreddit'] == filter_value]['title']

    cv = CountVectorizer(stop_words='english', ngram_range=ngram_range)
    df_cvec = DataFrame(
        # Fit and transform the vectorizer on our corpus
        cv.fit_transform(titles).toarray(),
        columns=cv.get_feature_names()
    )

    print(f'Count Vectorizer Result Shape: {df_cvec.shape}')
    print(f'Sample...\n{df_cvec.head(2)}\n...\n{df_cvec.tail(2)}\n')
    return df_cvec


def unigrams(df: DataFrame, df_2: DataFrame = None) -> set:

    print(r'+-----------------------------------+')
    print(r'|             Unigrams              |')
    print(r'+-----------------------------------+')

    # Set up variables to contain top 5 most used words
    df_top_5: Series = df.sum(axis=0).sort_values(ascending=False).head(5)
    df_top_5_set = set(df_top_5.index)
    print(f'\nDF:\n{df_top_5}')

    if df_2 is not None:
        df_2_top_5: Series = df_2.sum(
            axis=0).sort_values(ascending=False).head(5)
        df_2_top_5_set = set(df_2_top_5.index)
        print(f'\nDF 2:\n{df_2_top_5}')

    if df_2_top_5_set is not None:
        unigrams = df_top_5_set.intersection(df_2_top_5_set)
    else:
        unigrams = df_top_5_set

    print(f'Unigrams: {unigrams}')
    return unigrams


def get_stop_words(unigrams: list, bigrams: list) -> list:

    print(r'+-----------------------------------+')
    print(r'|            Stop Words             |')
    print(r'+-----------------------------------+')
    download('stopwords')
    custom = list(stopwords.words('english'))
    for i in unigrams:
        custom.append(i)

    for i in bigrams:
        split_words = i.split(" ")
        for word in split_words:
            custom.append(word)

    print(f'Stop Words: {len(custom)}\n{custom}')
    return custom

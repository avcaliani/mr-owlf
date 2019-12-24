from pandas import DataFrame, to_datetime, read_csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import stop_words


def count_vectorizer(df: DataFrame, filter_value: int, ngram_range: tuple = (1, 1)) -> DataFrame:

    print(r'+-----------------------------------+')
    print(r'|         Count Vectorizer          |')
    print(r'+-----------------------------------+')

    # Set variables to show only one category titles
    titles = df[df['subreddit'] == filter_value]['title']

    cv = CountVectorizer(stop_words = 'english', ngram_range=ngram_range)
    df_cvec = DataFrame(
        cv.fit_transform(titles).toarray(), # Fit and transform the vectorizer on our corpus
        columns=cv.get_feature_names()
    )

    print(f'Count Vectorizer Result Shape: {df_cvec.shape}')
    print(f'Sample...\n{df_cvec.head()}\n...\n{df_cvec.tail()}\n')


def unigrams(df: DataFrame, df_2: DataFrame = None) -> set:

    print(r'+-----------------------------------+')
    print(r'|             Unigrams              |')
    print(r'+-----------------------------------+')

    # Set up variables to contain top 5 most used words
    df_top_5: DataFrame = df.sum(axis = 0).sort_values(ascending=False).head(5)
    df_top_5_set = set(df_top_5.index)
    print(f'DF: {df_top_5}')

    if df_2 is not None:
        df_2_top_5: DataFrame = df_2.sum(axis = 0).sort_values(ascending=False).head(5)
        df_2_top_5_set = set(df_2_top_5.index)
        print(f'DF 2: {df_2_top_5}')

    # FIXME: Remove it ---------
    print(type(df_top_5))
    print(type(df_2_top_5))
    # --------------------------

    if df_2_top_5_set is not None:
        unigrams = df_top_5_set.intersection(df_2_top_5_set)
    else:
        unigrams = df_top_5_set

    print(f'Unigrams: {unigrams}')


def get_stop_words(unigrams: list, bigrams: list) -> list:

    print(r'+-----------------------------------+')
    print(r'|            Stop Words             |')
    print(r'+-----------------------------------+')
    
    custom = list(stop_words.ENGLISH_STOP_WORDS)
    for i in unigrams:
        custom.append(i)

    for i in bigrams:
        split_words = i.split(" ")
        for word in split_words:
            custom.append(word)
    
    return custom

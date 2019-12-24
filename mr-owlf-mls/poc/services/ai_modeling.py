from pandas import DataFrame
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

def try_out(df: DataFrame, stop_words: list) -> None:
    """Algotithms try out!

    We are expecting a model that is better than 54% and the majority class is 1 (TheOnion).
    If the model is not better than 54%, we know the model is not performing well.

    Model 01: Grid Search using 'Count Vectorizer' and 'Logistic Regression'
    Model 02: Grid Search using 'Tfidf Vectorizer' and 'Logistic Regression'
    Model 03: Grid Search using 'Count Vectorizer' and 'Multinomial Naive Bayes'
    Model 04: Grid Search using 'Tfidf Vectorizer' and 'Multinomial Naive Bayes'
    """

    print(r'+-----------------------------------+')
    print(r'|        Starting try out...        |')
    print(r'+-----------------------------------+')

    df['subreddit'].value_counts(normalize=True)

    X, y = df['title'], df['subreddit']
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, stratify=y)

    # Model 01 ---------------------------------------------------
    gs = GridSearchCV(
        Pipeline([
            ('cvec', CountVectorizer()),    
            ('lr', LogisticRegression(solver='liblinear'))
        ]),
        param_grid={
            'cvec__stop_words': [None, 'english', stop_words],
            'cvec__ngram_range': [(1,1), (2,2), (1,3)],
            'lr__C': [0.01, 1]
        },
        cv=3
    )
    gs.fit(X_train, y_train)
    show_score('01', gs, X_train, y_train, X_test, y_test)

    # Model 02 ---------------------------------------------------
    gs = GridSearchCV(
        Pipeline([
            ('tvect', TfidfVectorizer()),    
            ('lr', LogisticRegression(solver='liblinear'))
        ]),
        param_grid={
            'tvect__max_df': [.75, .98, 1.0],
            'tvect__min_df': [2, 3, 5],
            'tvect__ngram_range': [(1,1), (1,2), (1,3)],
            'lr__C': [1]
        },
        cv=3
    )
    gs.fit(X_train, y_train)
    show_score('02', gs, X_train, y_train, X_test, y_test)

    # Model 03 ---------------------------------------------------
    gs = GridSearchCV(
        Pipeline([
            ('cvec', CountVectorizer()),    
            ('nb', MultinomialNB())
        ]),
        param_grid={
            'cvec__ngram_range': [(1,1),(1,3)],
            'nb__alpha': [.36, .6]
        },
        cv=3
    )
    gs.fit(X_train, y_train)
    show_score('03', gs, X_train, y_train, X_test, y_test)

    # Model 04 ---------------------------------------------------
    gs = GridSearchCV(
        Pipeline([
            ('tvect', TfidfVectorizer()),    
            ('nb', MultinomialNB())
        ]),
        param_grid={
            'tvect__max_df': [.75, .98],
            'tvect__min_df': [4, 5],
            'tvect__ngram_range': [(1,2), (1,3)],
            'nb__alpha': [0.1, 1]
        },
        cv=5
    )
    gs.fit(X_train, y_train)
    show_score('04', gs, X_train, y_train, X_test, y_test)


def show_score(n: str, gs: GridSearchCV, X_train: DataFrame, y_train: DataFrame, X_test: DataFrame, y_test: DataFrame) -> None:
    print(r'+-----------------------------------+')
    print(f'|             Model {n}              |')
    print(r'+-----------------------------------+')
    print(f'\nBest Score  : {gs.best_score_}')
    print(f'Train Score : {gs.score(X_train, y_train)}')
    print(f'Test Score  : {gs.score(X_test, y_test)}')
    print(f'Best Params : {gs.best_params_}\n')
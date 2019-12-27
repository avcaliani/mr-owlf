from typing import Tuple
import numpy as np
from pandas import DataFrame
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.metrics import accuracy_score, recall_score, precision_score, confusion_matrix


def try_out(df: DataFrame, stop_words: list) -> None:
    """Algotithms try out!

    We are expecting a model that is better than 54% and the majority class is 1 (TheOnion).
    If the model is not better than 54%, we know the model is not performing well.

    Model 01: Grid Search using 'Count Vectorizer' and 'Logistic Regression'
    Model 02: Grid Search using 'Tfidf Vectorizer' and 'Logistic Regression'
    Model 03: Grid Search using 'Count Vectorizer' and 'Multinomial Naive Bayes'
    Model 04: Grid Search using 'Tfidf Vectorizer' and 'Multinomial Naive Bayes'
    """

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
    get_score('01', gs, X_train, y_train, X_test, y_test)

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
    get_score('02', gs, X_train, y_train, X_test, y_test)

    # Model 03 ---------------------------------------------------
    gs = GridSearchCV(
        Pipeline([
            ('cvec', CountVectorizer()),    
            ('nb', MultinomialNB())
        ]),
        param_grid={
            'cvec__stop_words': [None, 'english', stop_words],
            'cvec__ngram_range': [(1,1),(1,3)],
            'nb__alpha': [.36, .6]
        },
        cv=3
    )
    gs.fit(X_train, y_train)
    get_score('03', gs, X_train, y_train, X_test, y_test)

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
        cv=3
    )
    gs.fit(X_train, y_train)
    get_score('04', gs, X_train, y_train, X_test, y_test)


def naive_bayes(df: DataFrame, stop_words: list) -> Tuple[MultinomialNB, CountVectorizer]:
    """Train a Multinomial Naive Bayes classifier. We are going to use CountVectorizer and MultinomialNB."""
    
    print(r'+-----------------------------------+')
    print(r'|     Processing (Naive Bayes)      |')
    print(r'+-----------------------------------+')

    df['subreddit'].value_counts(normalize=True)
    X, y = df['title'], df['subreddit']
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, stratify=y)
    
    clf = MultinomialNB(alpha = 0.36)
    cv = CountVectorizer(ngram_range= (1, 3), stop_words = stop_words)

    cv.fit(X_train)

    Xcvec_train = cv.transform(X_train)
    Xcvec_test  = cv.transform(X_test)

    clf.fit(Xcvec_train, y_train)
    show_details(clf, Xcvec_train, y_train, Xcvec_test, y_test, clf.predict(Xcvec_test))
    return clf, cv


def logistic_regression(df: DataFrame, stop_words: list) -> Tuple[LogisticRegression, CountVectorizer]:
    """Train a Logistic Regression classifier. We are going to use CountVectorizer and MultinomialNB."""
    
    print(r'+-----------------------------------+')
    print(r'|  Processing (Logistic Regression) |')
    print(r'+-----------------------------------+')

    df['subreddit'].value_counts(normalize=True)
    X, y = df['title'], df['subreddit']
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, stratify=y)
    
    clf = LogisticRegression(C = 1.0, solver='liblinear')
    cv = CountVectorizer(stop_words = stop_words)

    cv.fit(X_train)

    Xcvec_train = cv.transform(X_train)
    Xcvec_test  = cv.transform(X_test)

    clf.fit(Xcvec_train, y_train)
    show_details(clf, Xcvec_train, y_train, Xcvec_test, y_test, clf.predict(Xcvec_test))
    return clf, cv


def show_details(clf, Xcvec_train, y_train, Xcvec_test, y_test, preds) -> None:

    cnf_matrix   = metrics.confusion_matrix(y_test, preds)
    tn_fp, fn_tp = np.array(cnf_matrix).tolist()
    tn, fp       = tn_fp
    fn, tp       = fn_tp

    print(f"Confusion Matrix\n{cnf_matrix}\n")
    print(f'Train Score            : {round(clf.score(Xcvec_train, y_train) * 100, 2)}%')
    print(f'Test Score             : {round(clf.score(Xcvec_test, y_test) * 100, 2)}%')
    print(f'Accuracy               : {round(metrics.accuracy_score(y_test, preds) * 100, 2)}%')
    print(f'Precision              : {round(metrics.precision_score(y_test, preds) * 100, 2)}%')
    print(f'Recall                 : {round(metrics.recall_score(y_test, preds) * 100, 2)}%')
    print(f'Specificity            : {round((tn/(tn+fp)) * 100, 2)}%')
    print(f'Misclassification Rate : {round((fp+fn)/(tn+fp+fn+tn) * 100, 2)}%')


def get_score(n, gs, X_train, y_train, X_test, y_test) -> any:
    
    score = {
        'best_score'   : round(gs.best_score_ * 100, 2),
        'train_score'  : round(gs.score(X_train, y_train) * 100, 2),
        'test_score'   : round(gs.score(X_test, y_test) * 100, 2),
        'classificator': None,
        'vectorizer'   : None
    }
    
    print(r'+-----------------------------------+')
    print(f'|             Model {n}              |')
    print(r'+-----------------------------------+')
    
    print(f'\nBest Score  : {score["best_score"]}%')
    print(f'Train Score : {score["train_score"]}%')
    print(f'Test Score  : {score["test_score"]}%')
    print(f'Best Params : {gs.best_params_}\n')

    return score

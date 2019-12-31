from typing import Tuple, List

import numpy as np
from pandas import DataFrame
from sklearn import metrics
from sklearn.model_selection import train_test_split

from service.ai.factory import AIFactory


def get_model(df: DataFrame, stop_words: List) -> Tuple[any, any]:

    df['subreddit'].value_counts(normalize=True)
    x, y = df['title'], df['subreddit']

    factory = AIFactory(x, y, stop_words)
    clf, vectorizer, gs_score = factory.get_classifier()

    X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=42, stratify=y)

    vectorizer.fit(X_train)

    Xcvec_train = vectorizer.transform(X_train)
    Xcvec_test = vectorizer.transform(X_test)

    clf.fit(Xcvec_train, y_train)
    show_details(clf, vectorizer, gs_score, Xcvec_train, y_train, Xcvec_test, y_test, clf.predict(Xcvec_test))
    return clf, vectorizer


def show_details(clf, vectorizer, gs_score, Xcvec_train, y_train, Xcvec_test, y_test, preds) -> None:

    cnf_matrix = metrics.confusion_matrix(y_test, preds)
    tn_fp, fn_tp = np.array(cnf_matrix).tolist()
    tn, fp = tn_fp
    fn, tp = fn_tp

    print(f'Classifier               : {type(clf).__name__}')
    print(f'Vectorizer               : {type(vectorizer).__name__}')
    print(f'Best Params              : {gs_score["best_params"]}%')
    print(f'Best Score (Grid Search) : {gs_score["best_score"]}')
    print(f'Train Score              : {round(clf.score(Xcvec_train, y_train) * 100, 2)}%')
    print(f'Test Score               : {round(clf.score(Xcvec_test, y_test) * 100, 2)}%')
    print(f'Accuracy                 : {round(metrics.accuracy_score(y_test, preds) * 100, 2)}%')
    print(f'Precision                : {round(metrics.precision_score(y_test, preds) * 100, 2)}%')
    print(f'Recall                   : {round(metrics.recall_score(y_test, preds) * 100, 2)}%')
    print(f'Specificity              : {round((tn / (tn + fp)) * 100, 2)}%')
    print(f'Misclassification Rate   : {round((fp + fn) / (tn + fp + fn + tn) * 100, 2)}%')
    print(f'Confusion Matrix\n{DataFrame(cnf_matrix).head()}\n')

from logging import getLogger
from typing import List, Tuple

from pandas import Series
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


class MLFactory:
    """
    Algorithms factory.
    We are expecting a model that is better than 54% and the majority class is 1 (TheOnion).
    If the model is not better than 54%, we know the model is not performing well.

    Model 01: Grid Search using 'Count Vectorizer' and 'Logistic Regression'
    Model 02: Grid Search using 'Tfidf Vectorizer' and 'Logistic Regression'
    Model 03: Grid Search using 'Count Vectorizer' and 'Naive Bayes'
    Model 04: Grid Search using 'Tfidf Vectorizer' and 'Naive Bayes'
    """

    def __init__(self, x: Series, y: Series, stop_words: List):
        """
        Default constructor.
        :param x: Data
        :param y: Classes for each datum
        :param stop_words: Stop Words
        """
        self.log = getLogger('root')
        self.best_model = None
        self.stop_words = stop_words
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            x, y, random_state=42, stratify=y
        )

    def get_classifier(self) -> Tuple[any, any, any]:
        """
        Return the best evaluated model and vectorizer.
        :return: Tuple[Classifier, Vectorizer, Score Object]
        """
        if self.best_model is not None:
            return self.best_model

        models = [
            self.model_01(),
            self.model_02(),
            self.model_03(),
            self.model_04()
        ]
        self.best_model = sorted(models, key=lambda v: v[2]['best_score'], reverse=True)[0]

        self.log.info(f'The best model is {type(self.best_model[0]).__name__} with {type(self.best_model[1]).__name__}')
        return self.best_model

    def model_01(self) -> Tuple[any, any, any]:
        self.log.info(f'[LOGISTIC REGRESSION] [COUNT VECTORIZER]')
        gs = GridSearchCV(
            Pipeline([
                ('cvec', CountVectorizer()),
                ('lr', LogisticRegression(solver='liblinear'))
            ]),
            param_grid={
                'cvec__stop_words': [None, 'english', self.stop_words],
                'cvec__ngram_range': [(1, 1), (2, 2), (1, 3)],
                'lr__C': [0.01, 1]
            },
            cv=3
        )
        gs.fit(self.X_train, self.y_train)

        gs_score = self.get_gs_score(gs)
        params = gs_score['best_params']

        clf = LogisticRegression(C=params['lr__C'], solver='liblinear')
        vectorizer = CountVectorizer(
            ngram_range=params['cvec__ngram_range'],
            stop_words=params['cvec__stop_words']
        )
        return clf, vectorizer, gs_score

    def model_02(self) -> Tuple[any, any, any]:
        self.log.info(f'[LOGISTIC REGRESSION] [TFIDF VECTORIZER]')
        gs = GridSearchCV(
            Pipeline([
                ('tvect', TfidfVectorizer()),
                ('lr', LogisticRegression(solver='liblinear'))
            ]),
            param_grid={
                'tvect__max_df': [.75, .98, 1.0],
                'tvect__min_df': [2, 3, 5],
                'tvect__ngram_range': [(1, 1), (1, 2), (1, 3)],
                'lr__C': [1]
            },
            cv=3
        )
        gs.fit(self.X_train, self.y_train)

        gs_score = self.get_gs_score(gs)
        params = gs_score['best_params']

        clf = LogisticRegression(C=params['lr__C'], solver='liblinear')
        vectorizer = TfidfVectorizer(
            max_df=params['tvect__max_df'],
            min_df=params['tvect__min_df'],
            ngram_range=params['tvect__ngram_range'],
            stop_words=self.stop_words
        )
        return clf, vectorizer, gs_score

    def model_03(self) -> Tuple[any, any, any]:
        self.log.info(f'[MULTINOMIAL NB] [COUNT VECTORIZER]')
        gs = GridSearchCV(
            Pipeline([
                ('cvec', CountVectorizer()),
                ('nb', MultinomialNB())
            ]),
            param_grid={
                'cvec__stop_words': [None, 'english', self.stop_words],
                'cvec__ngram_range': [(1, 1), (1, 3)],
                'nb__alpha': [.36, .6]
            },
            cv=3
        )
        gs.fit(self.X_train, self.y_train)

        gs_score = self.get_gs_score(gs)
        params = gs_score['best_params']

        clf = MultinomialNB(alpha=params['nb__alpha'])
        vectorizer = CountVectorizer(
            ngram_range=params['cvec__ngram_range'],
            stop_words=params['cvec__stop_words']
        )
        return clf, vectorizer, gs_score

    def model_04(self) -> Tuple[any, any, any]:
        self.log.info(f'[MULTINOMIAL NB] [TFIDF VECTORIZER]')
        gs = GridSearchCV(
            Pipeline([
                ('tvect', TfidfVectorizer()),
                ('nb', MultinomialNB())
            ]),
            param_grid={
                'tvect__max_df': [.75, .98],
                'tvect__min_df': [4, 5],
                'tvect__ngram_range': [(1, 2), (1, 3)],
                'nb__alpha': [0.1, 1]
            },
            cv=3
        )
        gs.fit(self.X_train, self.y_train)

        gs_score = self.get_gs_score(gs)
        params = gs_score['best_params']

        clf = MultinomialNB(alpha=params['nb__alpha'])
        vectorizer = TfidfVectorizer(
            max_df=params['tvect__max_df'],
            min_df=params['tvect__min_df'],
            ngram_range=params['tvect__ngram_range'],
            stop_words=self.stop_words
        )
        return clf, vectorizer, gs_score

    def get_gs_score(self, gs: GridSearchCV) -> any:
        score = {
            'best_score': round(gs.best_score_ * 100, 2),
            'best_params': gs.best_params_,
        }
        self.log.info(f'Best Score  : {score["best_score"]}%')
        self.log.info(f'Train Score : {round(gs.score(self.X_train, self.y_train) * 100, 2)}%')
        self.log.info(f'Test Score  : {round(gs.score(self.X_test, self.y_test) * 100, 2)}%')
        self.log.info(f'Best Params : {score["best_params"]}\n')
        return score

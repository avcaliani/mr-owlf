from logging import getLogger

from pandas import DataFrame
from pymongo.database import Database
from repository.author import AuthorRepository
from repository.domain import DomainRepository

FAKE = '0'
NOT_FAKE = '1'


class Process:

    def __init__(self, clf: any, vectorizer: any, db: Database):
        self.log = getLogger('root')
        self.clf = clf
        self.vectorizer = vectorizer
        self.author_repository = AuthorRepository(db)
        self.domain_repository = DomainRepository(db)

    def run(self, **kwargs) -> float:
        """Calculate news score.

        If no arguments are passed it will return "0.0" as score.

        Keyword Args
        ------------
        sentence     (str): News sentence
        author       (str): Author(s) name(s)
        domain       (str): News domain
        publish_date (str): The date that it was published
        """
        score = 0.0
        if len(kwargs) == 0:
            return score

        if 'sentence' in kwargs:
            score = score + (self.sentence_score(kwargs.get('sentence')) * 1.0)

        if 'author' in kwargs:
            score = score + (self.author_score(kwargs.get('author')) * 1.25)

        if 'domain' in kwargs:
            score = score + (self.domain_score(kwargs.get('domain')) * 1.25)

        if 'publish_date' in kwargs:
            score = score + (self.publish_date_score(kwargs.get('publish_date')) * 0.5)

        score = float(score / 4)
        self.log.info(f'[FINAL SCORE] "{score}"')
        return score

    def sentence_score(self, sentence: str) -> float:
        data = DataFrame({'title': [sentence]})

        data_cvec = self.vectorizer.transform(data['title'])
        preds_prob = self.clf.predict_proba(data_cvec)

        fake = '{0:.2f}'.format(preds_prob[0][0])
        not_fake = '{0:.2f}'.format(preds_prob[0][1])
        self.log.info(f'[SENTENCE]\n"{sentence}"\nProb. to be Fake "{fake}" / Not Fake "{not_fake}"')
        return float(preds_prob[0][1])

    def author_score(self, author_name: str) -> float:
        author = self.author_repository.find(author_name)
        if author is None or 'classification' not in author:
            return 0.0

        clf = author['classification']
        good = int(clf[NOT_FAKE]) if NOT_FAKE in clf else 0
        bad = int(clf[FAKE]) if FAKE in clf else 0
        total = good + bad
        score = 5.0 if total == 0 else float(good / total)

        self.log.info(f'[AUTHOR] "{author_name}" score is "{score}"')
        return score

    def domain_score(self, domain_name: str) -> float:
        domain = self.domain_repository.find(domain_name)
        if domain is None or 'classification' not in domain:
            return 0.0

        clf = domain['classification']
        good = int(clf[NOT_FAKE]) if NOT_FAKE in clf else 0
        bad = int(clf[FAKE]) if FAKE in clf else 0
        total = good + bad
        score = 5.0 if total == 0 else float(good / total)

        self.log.info(f'[DOMAIN] "{domain_name}" score is "{score}"')
        return score

    def publish_date_score(self, date: str) -> float:
        # TODO: Do it
        return 0.0

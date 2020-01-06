from logging import getLogger

from pandas import DataFrame


class Process:

    def __init__(self, clf: any, vectorizer: any):
        self.log = getLogger('root')
        self.clf = clf
        self.vectorizer = vectorizer

    def run(self, sentence: str) -> any:
        self.log.info(f'[PROCESS]')
        self.log.info(f'Sentence => "{sentence}"')
        data = DataFrame({'title': [sentence]})

        data_cvec = self.vectorizer.transform(data['title'])
        preds_prob = self.clf.predict_proba(data_cvec)

        fake = '{0:.2f}'.format(preds_prob[0][0])
        not_fake = '{0:.2f}'.format(preds_prob[0][1])
        self.log.info(f'Prob. to be Fake "{fake}" / Not Fake "{not_fake}"')
        return not_fake

import pickle

from pymongo.database import Database
from service.process import Process
from util import database

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'


def load(file: str) -> any:
    _file = open(file, 'rb')
    obj = pickle.load(_file)
    _file.close()
    return obj


if __name__ == '__main__':

    db: Database = database.connect()['mr-owlf-db']
    clf = load('./classifier.pkl')
    vectorizer = load('./vectorizer.pkl')

    sentences = [
        (
            'more people should have donated wikipedia has announced they will be forced to take down their entry for ostrich due to lack of funding',
            'dwaxe',
            'news.clickhole.com',
            '2019-08-10',
            'NOT_FAKE'
        ),
        (
            'trump aides investigating whistleblower struggling to identify single person in cia with moral principles',
            'aresef',
            'politics.theonion.com',
            '2019-12-20',
            'NOT_FAKE'
        ),
        (
            'new york times offers to disclose whistleblower identity to readers who subscribe in next hours',
            'Live_Think_Diagnosis',
            'theonion.com',
            '2019-01-19',
            'NOT_FAKE'
        ),
        (
            'new hellmann s theme park to feature world s longest lazy mayo river',
            'aresef',
            'theonion.com',
            '2019-01-19',
            'NOT_FAKE'
        )
    ]

    process = Process(clf, vectorizer, db)
    for sentence in sentences:
        score = process.run(
            sentence=sentence[0],
            author=sentence[1],
            domain=sentence[2],
            publish_date=sentence[3]
        )
        print(f'Score: {score}')

import pickle
from logging import StreamHandler, Formatter, getLogger, DEBUG

from pymongo.database import Database
from service.process import Process
from util import database

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'


def init_log():
    logger = getLogger('root')
    logger.setLevel(DEBUG)
    _console = StreamHandler()
    _console.setLevel(DEBUG)
    _console.setFormatter(Formatter(fmt='\033[1;35;40m[SAMPLE] \033[1;32;40m[%(levelname)s]\033[0m %(message)s'))
    logger.addHandler(_console)


def load(file: str) -> any:
    _file = open(file, 'rb')
    obj = pickle.load(_file)
    _file.close()
    return obj


if __name__ == '__main__':

    init_log()
    db: Database = database.connect()['mr-owlf-db']
    clf = load('./classifier.pkl')
    vectorizer = load('./vectorizer.pkl')

    sentences = [
        (
            "A Wikipedia anunciou que será forçada a retirar a inscrição para 'Ostrich' devido à falta de financiamento.",
            'dwaxe',
            'news.clickhole.com',
            '2019-08-10',
            'NOT_FAKE'
        ),
        (
            'Assessores de Trump investigam denunciante que luta para identificar uma única pessoa na CIA com princípios morais.',
            'aresef',
            'politics.theonion.com',
            '2019-12-20',
            'NOT_FAKE'
        ),
        (
            'Ofertas do "New York Times" para divulgar a identidade dos denunciantes aos leitores que se inscreverem nas próximas 24 horas.',
            'Live_Think_Diagnosis',
            'theonion.com',
            '2019-01-19',
            'NOT_FAKE'
        ),
        (
            'Novo parque temático de Hellmann contará com o rio Mayo mais longo e preguiçoso do mundo.',
            'aresef',
            'theonion.com',
            '2019-01-19',
            'NOT_FAKE'
        ),
        (
            'Trump diz que a China deve investigar os Bidens e dobra sua investigação na Ucrânia.',
            'not_slim_shaddy',
            'cnbc.com',
            '2019-01-19',
            'FAKE'
        ),
        (
            'Russo processa Apple por "torná-lo gay" depois de receber 69 GayCoin em vez de Bitcoin.',
            'ShkekeA doctor donated sperm 30 years ago. Now he has at least 17 kids, lawsuit alleges',
            'telegraph.co.uk',
            '2019-01-19',
            'FAKE'
        ),
        (
            'Um médico doou esperma há 30 anos, agora ele tem pelo menos 17 filhos.',
            'raymf',
            'fox13now.com',
            '2019-01-19',
            'FAKE'
        ),
        (
            'Ex-engenheiro do Yahoo foi preso por invadir 6.000 contas à procura de fotos e vídeos íntimos',
            'Nawaao',
            'mazechmedia.com',
            '2019-01-19',
            'FAKE'
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

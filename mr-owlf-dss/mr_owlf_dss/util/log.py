from os import environ as env
from logging import StreamHandler, FileHandler, Formatter, getLogger, DEBUG, INFO

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'

APP_ENV = env.get('MR_OWLF_ENV', 'DEV')
LOG_FILE = env.get('MR_OWLF_LOG_FILE', './dss.log')


def init():

    # Console Handler
    _console = StreamHandler()
    _console.setLevel(DEBUG)
    _console.setFormatter(Formatter(
        fmt='%(levelname)s\t:: %(asctime)s :: %(message)s',
        datefmt='%y.%m.%d %H:%M:%S'
    ))

    # File Handler
    _file = FileHandler(LOG_FILE, mode='w+', encoding='utf8')
    _file.setLevel(INFO)
    _file.setFormatter(Formatter(
        fmt='%(levelname)s\t:: %(asctime)s :: (%(name)s) %(message)s',
        datefmt='%y.%m.%d %H:%M:%S'
    ))

    logger = getLogger('root')
    logger.setLevel(DEBUG)
    logger.addHandler(_file)
    if APP_ENV == 'DEV':
        logger.addHandler(_console)

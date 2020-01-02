from os import environ as env
from logging import StreamHandler, FileHandler, Formatter, getLogger, DEBUG, INFO

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'

APP_ENV = env.get('MR_OWLF_ENV', 'DEV')
LOG_FILE = env.get('MR_OWLF_LOG_FILE', './mr-owlf-dss.log')


def init() -> None:

    # Console Handler
    _console = StreamHandler()
    _console.setLevel(DEBUG)
    _console.setFormatter(Formatter(
        fmt='\033[1;36;40m[%(asctime)s]\033[1;32;40m[%(levelname)s]\033[0m %(message)s',
        datefmt='%y.%m.%d %H:%M:%S'
    ))

    # File Handler
    _file = FileHandler(LOG_FILE, mode='w+', encoding='utf8')
    _file.setLevel(INFO)
    _file.setFormatter(Formatter(
        fmt='[%(asctime)s][%(levelname)s] %(message)s',
        datefmt='%y.%m.%d %H:%M:%S'
    ))

    logger = getLogger('root')
    logger.setLevel(DEBUG)
    logger.addHandler(_file)
    if APP_ENV == 'DEV':
        logger.addHandler(_console)

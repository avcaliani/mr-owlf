from logging import StreamHandler, FileHandler, Formatter, getLogger, DEBUG, INFO
from os import environ as env

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'

LOG_LEVEL = DEBUG if env.get('APP_LOG_LEVEL', 'DEBUG') == 'DEBUG' else INFO
LOG_FILE = env.get('APP_LOG_FILE', './mr-owlf-mls.log')


def init() -> None:
    # Console Handler
    _console = StreamHandler()
    _console.setLevel(LOG_LEVEL)
    _console.setFormatter(Formatter(
        fmt='\033[1;36;40m[%(asctime)s]\033[1;32;40m[%(levelname)s]\033[0m %(message)s',
        datefmt='%y.%m.%d %H:%M:%S'
    ))

    # File Handler
    _file = FileHandler(LOG_FILE, mode='w+', encoding='utf8')
    _file.setLevel(LOG_LEVEL)
    _file.setFormatter(Formatter(
        fmt='[%(asctime)s][%(levelname)s] %(message)s',
        datefmt='%y.%m.%d %H:%M:%S'
    ))

    logger = getLogger('root')
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(_file)
    logger.addHandler(_console)

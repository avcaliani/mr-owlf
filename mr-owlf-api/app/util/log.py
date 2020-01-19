from logging import StreamHandler, Formatter, getLogger, DEBUG


def init() -> None:
    """
    Initialize log configuration.
    """
    console = StreamHandler()
    console.setLevel(DEBUG)
    console.setFormatter(Formatter(
        fmt='\033[1;36;40m[%(asctime)s]\033[1;32;40m[%(levelname)s]\033[0m %(message)s',
        datefmt='%y.%m.%d %H:%M:%S'
    ))

    logger = getLogger('root')
    logger.setLevel(DEBUG)
    logger.addHandler(console)

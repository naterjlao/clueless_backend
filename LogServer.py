import logging

LEVEL = logging.DEBUG
HANDLER = logging.StreamHandler()
HANDLER.setLevel(LEVEL)


def logger(name):

    log = logging.getLogger(name)
    log.setLevel(LEVEL)
    log.addHandler(HANDLER)

    return log
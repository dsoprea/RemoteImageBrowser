import os
import logging

_IS_DEBUG = bool(int(os.environ.get('DEBUG', '1')))

def configure():
    rootLogger = logging.getLogger()

    if _IS_DEBUG:
        rootLogger.setLevel(logging.DEBUG)
    else:
        rootLogger.setLevel(logging.INFO)

    sh = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(name)s %(levelname)s] %(message)s')
    sh.setFormatter(formatter)
    rootLogger.addHandler(sh)

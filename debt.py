import datetime
from logging import INFO
from logging import basicConfig
from logging import getLogger

from arrow import now

if __name__ == '__main__':
    TIME_START = now()
    size = 17 * (TIME_START.date() - datetime.date(year=2001, month=1, day=1)).days // 30
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    LOGGER.info('started')

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))

import datetime
from logging import INFO
from logging import basicConfig
from logging import getLogger

from arrow import now
from pandas import read_csv

BASE_URL = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/'
DAY = 31
ENDPOINT = 'v2/accounting/od/debt_to_penny'
FIELDS = 'record_date,debt_held_public_amt,intragov_hold_amt,tot_pub_debt_out_amt,'
FORMAT = 'csv'
MONTH = 3
YEAR = 2005

if __name__ == '__main__':
    TIME_START = now()
    our_filter = 'record_date:gte:{}-{:02d}-{:02d}'.format(YEAR, MONTH, DAY)
    size = 1 * (TIME_START.date() - datetime.date(year=YEAR, month=MONTH, day=DAY)).days
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    LOGGER.info('started')

    url = '{}{}?fields={}&filter={}&format={}&page[size]={}'.format(BASE_URL, ENDPOINT, FIELDS, our_filter,
                                                                    FORMAT, size)

    LOGGER.info('url: %s', url)
    data_df = read_csv(filepath_or_buffer=url)
    LOGGER.info('shape: %s', data_df.shape)
    LOGGER.info('data headings: %s', list(data_df))

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))

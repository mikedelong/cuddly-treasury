from logging import INFO
from logging import basicConfig
from logging import getLogger

from arrow import now
from pandas import read_csv

BASE_URL = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/'
ENDPOINT = 'v2/accounting/od/avg_interest_rates'
FIELDS = 'record_date,security_type_desc,security_desc,avg_interest_rate_amt,src_line_nbr,'
FILTER = 'record_date:gte:2015-01-01'
FORMAT = 'csv'
SIZE = 5000

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    LOGGER.info('started')

    url = '{}{}?fields={}&filter={}&format={}&page[size]={}'.format(BASE_URL, ENDPOINT, FIELDS, FILTER,
                                                                    FORMAT, SIZE)
    LOGGER.info('url: %s', url)
    data_df = read_csv(filepath_or_buffer=url)
    LOGGER.info('shape: %s', data_df.shape)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))

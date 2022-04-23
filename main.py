from pandas import DataFrame
from requests import get
from logging import INFO
from logging import basicConfig
from logging import getLogger
from arrow import now

BASE_URL = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/'
ENDPOINT = 'v2/accounting/od/avg_interest_rates'
FILTER = 'record_date:gte:2015-01-01'
FIELDS = 'record_date,security_type_desc,security_desc,avg_interest_rate_amt,src_line_nbr,'

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    LOGGER.info('started')

    url = '{}{}?fields={}&filter={}'.format(BASE_URL, ENDPOINT, FIELDS, FILTER)
    LOGGER.info('url: %s', url)
    response = get(url=url)
    data = response.json()['data']
    LOGGER.info('count: %d', len(data))
    data_df = DataFrame.from_records(data=data, index=None, exclude=None)
    LOGGER.info('shape: %s', data_df.shape)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))

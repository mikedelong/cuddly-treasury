import datetime
from logging import INFO
from logging import basicConfig
from logging import getLogger

from arrow import now
from pandas import read_csv
from plotly.express import line

BASE_URL = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/'
COLUMNS = {'record_date': 'date', 'value': 'dollars'}
DAY = 31
ENDPOINT = 'v2/accounting/od/debt_to_penny'
FIELDS = 'record_date,debt_held_public_amt,intragov_hold_amt,tot_pub_debt_out_amt,'
FORMAT = 'csv'
MONTH = 3
YEAR = 2005

if __name__ == '__main__':
    TIME_START = now()
    size = 1 * (TIME_START.date() - datetime.date(year=YEAR, month=MONTH, day=DAY)).days
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    LOGGER.info('started')

    our_filter = 'record_date:gte:{}-{:02d}-{:02d}'.format(YEAR, MONTH, DAY)
    url = '{}{}?fields={}&filter={}&format={}&page[size]={}'.format(BASE_URL, ENDPOINT, FIELDS, our_filter,
                                                                    FORMAT, size)

    LOGGER.info('url: %s', url)
    data_df = read_csv(filepath_or_buffer=url)
    LOGGER.info('shape: %s', data_df.shape)
    LOGGER.info('data headings: %s', list(data_df))
    figure = line(data_frame=data_df.melt(id_vars=['record_date'],
                                          value_vars=['debt_held_public_amt', 'intragov_hold_amt',
                                                      'tot_pub_debt_out_amt'],
                                          ).rename(columns=COLUMNS),
                  facet_col='variable', x='date', y='dollars')
    figure.show()

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))

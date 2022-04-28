import datetime
from logging import INFO
from logging import basicConfig
from logging import getLogger

from arrow import now
from pandas import read_csv

import plotly.express as px

BASE_URL = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/'
ENDPOINT = 'v2/accounting/od/avg_interest_rates'
FIELDS = 'record_date,security_type_desc,security_desc,avg_interest_rate_amt,src_line_nbr,'
FILTER = 'record_date:gte:2001-01-01'
FORMAT = 'csv'
SECURITY = 'security_desc'

if __name__ == '__main__':
    TIME_START = now()
    size = 17 * (TIME_START.date() - datetime.date(year=2001, month=1, day=1)).days // 30
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    LOGGER.info('started')

    url = '{}{}?fields={}&filter={}&format={}&page[size]={}'.format(BASE_URL, ENDPOINT, FIELDS, FILTER,
                                                                    FORMAT, size)
    LOGGER.info('url: %s', url)
    data_df = read_csv(filepath_or_buffer=url)
    LOGGER.info('shape: %s', data_df.shape)

    LOGGER.info('data headings: %s', list(data_df))
    security_types = sorted(data_df[SECURITY].unique())
    for security_type in security_types:
        LOGGER.info('%s : %d', security_type, len(data_df[data_df[SECURITY] == security_type]))

    # remove the series we don't care about
    remove = ['Hope Bonds', 'R.E.A. Series', 'Treasury Inflation-Indexed Bonds',
              'Treasury Inflation-Indexed Notes']
    data_df = data_df[~data_df['security_desc'].isin(remove)]
    # fix one weird datapoint
    data_df['security_desc'] = data_df['security_desc'].apply(
        lambda x: x if x != 'TotalMarketable' else 'Total Marketable')

    use_columns = ['record_date', 'security_desc', 'avg_interest_rate_amt']
    map_columns = {'record_date': 'date', 'avg_interest_rate_amt': 'rate'}
    figure = px.line(data_frame=data_df[use_columns].rename(columns=map_columns), x='date',
                     facet_col='security_desc', facet_col_wrap=3, y='rate', )
    figure.show()

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))

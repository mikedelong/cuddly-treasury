from pandas import DataFrame
from requests import get

BASE_URL = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/'
ENDPOINT = 'v2/accounting/od/avg_interest_rates'
FILTER = 'record_date:gte:2015-01-01'
FIELDS = 'record_date,security_type_desc,security_desc,avg_interest_rate_amt,src_line_nbr,'

if __name__ == '__main__':
    url = '{}{}?fields={}&filter={}'.format(BASE_URL, ENDPOINT, FIELDS, FILTER)
    print(url)
    response = get(url=url)
    data = response.json()['data']
    print(type(data))
    print(len(data))
    data_df = DataFrame.from_records(data=data, index=None, exclude=None)
    print(data_df.shape)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

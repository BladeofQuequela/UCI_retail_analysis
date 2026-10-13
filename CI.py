import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
import sqlalchemy as sql
import os
from statsmodels.stats.proportion import proportion_confint
from statsmodels.stats.proportion import proportions_ztest
import itertools

os.environ['LC_MESSAGES'] = 'C'
os.environ['PGCLIENTENCODING'] = 'UTF8'

url = sql.URL.create (
    drivername='postgresql+psycopg2',
    username = 'postgres',
    password = 'ptgrs342',
    host = 'localhost',
    port = '5432',
    database = 'crm'
)
engine = sql.create_engine(url, connect_args={'client_encoding': 'UTF8', 'options': '-c lc_messages=C'})

df = pd.read_sql('SELECT  first_month, total_customers, cohort_total, retention FROM arpu_cltv WHERE lifetime_month = 1', engine)

df['ci_low'], df['ci_high'] = proportion_confint(
    count=df['total_customers'],
    nobs=df['cohort_total'],
    alpha=0.05,
    method='wilson'
)

df['ci_low'] = (df['ci_low']*100).round(1)
df['ci_high'] = (df['ci_high']*100).round(1)

results = []

for (i,row1), (j,row2) in itertools.combinations(df.iterrows(), 2):
    z, p = proportions_ztest(
        count = [row1['total_customers'], row2['total_customers']],
        nobs = [row1['cohort_total'], row2['cohort_total']],
        alternative = 'two-sided',
    )
    results.append({
        'cohort_1': row1['first_month'].strftime('%Y-%m'),
        'cohort_2': row2['first_month'].strftime('%Y-%m'),
        'p_value': round(p, 4)
    })

result_df = pd.DataFrame(results)
significant = result_df[result_df['p_value'] < 0.05]
print(significant)
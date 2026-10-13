import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
import sqlalchemy as sql
import os
import seaborn as sns
import matplotlib.pyplot as plt

os.environ['LC_MESSAGES'] = 'C'
os.environ['PGCLIENTENCODING'] = 'UTF8'

from db import engine

df = pd.read_sql('SELECT * FROM arpu_cltv', engine)
print(df)

cohort_pivot = df.pivot(index = 'first_month',
         columns = 'lifetime_month',
         values = 'cum_ltv'
         )

cohort_pivot.index = cohort_pivot.index.strftime('%b %Y')

plt.figure(figsize = (12,8))
sns.heatmap(cohort_pivot, annot=True, fmt='.2f', cmap='Oranges', linewidths=0.5, linecolor='white')
plt.title('Cumulative LTV by Cohort')
plt.ylabel('Cohort')
plt.xlabel('Lifetime month')
plt.figtext(0.5, 0.01, 'Units: GBP (£)', ha='center', fontsize=10, style='italic')
plt.savefig('images/ltv_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()

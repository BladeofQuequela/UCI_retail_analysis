#Гипотеза – когорты с высоким retention приносят больше денег.

import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
import sqlalchemy as sql
import os
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
import seaborn as sns

os.environ['LC_MESSAGES'] = 'C'
os.environ['PGCLIENTENCODING'] = 'UTF8'

from db import engine

df = pd.read_sql('SELECT  first_month, total_customers, retention, cum_ltv FROM arpu_cltv WHERE lifetime_month = 1', engine)

r_pearson, p_pearson = pearsonr(df['retention'], df['cum_ltv'])
r_spearman, p_spearman = spearmanr(df['retention'], df['cum_ltv'])

print(f'Pearson:  r = {r_pearson:.3f}, p = {p_pearson:.4f}')
print(f'Spearman: r = {r_spearman:.3f}, p = {p_spearman:.4f}')



plt.figure(figsize=(10, 6))
sns.regplot(data=df, x='retention', y='cum_ltv',
            scatter_kws={'s': 100, 'color': 'steelblue'},
            line_kws={'color': 'red'})
plt.title('Correlation: Retention (Month 1) vs Cumulative LTV (Month 1)')
plt.xlabel('Retention, %')
plt.ylabel('Cumulative LTV, GBP')
plt.grid(alpha=0.3)
plt.figtext(0.5, 0.01, 'n = 8 cohorts',
            ha='center', fontsize=9, style='italic')
plt.savefig('images/ret_lvt_cor.png', dpi=150, bbox_inches='tight')
plt.show()


#Зависит ли XYZ (стабильность) от ABC (выручки) по товару? Гипотеза: независимы

import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
import sqlalchemy as sql
import os
from scipy.stats import chi2_contingency
import numpy as np

os.environ['LC_MESSAGES'] = 'C'
os.environ['PGCLIENTENCODING'] = 'UTF8'

from db import engine

df = pd.read_sql('SELECT * FROM abc_xyz_revenue', engine)

contingency = df.groupby(['abc_class', 'xyz_class'])['stockcode'].count().unstack(fill_value=0)
contingency = contingency.reindex(index=['A','B','C'], columns=['X','Y','Z'], fill_value=0)
print(contingency)

chi2, p, dof, expected = chi2_contingency(contingency)
print(f'Chi2: {chi2:.2f}')
print(f'p-value: {p:.4f}')
print(f'Degrees of freedom: {dof}')

n = contingency.values.sum()
cramers_v = np.sqrt(chi2 / (n * (min(contingency.shape) - 1)))
print(f"Cramér's V: {cramers_v:.3f}")

contingency_pct = contingency.div(contingency.sum(axis=1), axis=0) * 100
contingency_pct.plot(kind='bar', stacked=True, figsize=(8, 6), colormap='viridis')
plt.title('XYZ Distribution within each ABC Class')
plt.ylabel('Percentage, %')
plt.xlabel('ABC Class')
plt.show()

#анализ носит крайне ограниченный смысл из-за огромной доли Z. Возможно, пересчитать по выручке, а не количеству? Тут и считаем, собсвтвенно
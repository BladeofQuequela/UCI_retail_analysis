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

df = pd.read_sql('SELECT * FROM abc_xyz_matrix', engine)
print(df)

matrix_revenue = df.groupby(['abc_class','xyz_class'])['revenue'].sum().reset_index()
pivot = matrix_revenue.pivot(index = 'abc_class',
         columns = 'xyz_class',
         values = 'revenue'
         )
pivot = pivot.reindex(index=['A', 'B', 'C'], columns=['X', 'Y', 'Z'])/1000000

print(pivot)

plt.figure(figsize = (12,8))
sns.heatmap(pivot, annot=True, fmt='.2f', cmap='Oranges', linewidths=0.5, linecolor='white')
plt.title('ABC/XYZ spread')
plt.ylabel('ABC')
plt.xlabel('XYZ')
plt.figtext(0.5, 0.01, 'Units: Million GBP (£) | Source: UCI Online Retail Dataset',
            ha='center', fontsize=10, style='italic', color='gray')
plt.savefig('images/abc_xyz_revenue.png', dpi=150, bbox_inches='tight')
plt.show()


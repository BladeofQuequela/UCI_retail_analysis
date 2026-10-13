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

matrix = df.groupby(['abc_class','xyz_class'])['stockcode'].count().reset_index()
pivot = matrix.pivot(index = 'abc_class',
         columns = 'xyz_class',
         values = 'stockcode'
         )
pivot = pivot.reindex(index=['A', 'B', 'C'], columns=['X', 'Y', 'Z'])

print(pivot)

plt.figure(figsize = (12,8))
sns.heatmap(pivot, annot=True, fmt='.2f', cmap='Blues', linewidths=0.5, linecolor='white')
plt.title('ABC/XYZ by SKU count')
plt.ylabel('ABC')
plt.xlabel('XYZ')
plt.savefig('images/abc_xyz_count.png', dpi=150, bbox_inches='tight')
plt.show()

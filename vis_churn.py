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

df_churn = pd.read_sql('SELECT * FROM churn', engine)

plt.figure(figsize=(12, 6))
plt.hist(df_churn['difference'], bins=50, color='steelblue', edgecolor='white')
plt.title('Distribution of Days Since Last Purchase')
plt.xlabel('Days Since Last Purchase')
plt.ylabel('Number of Customers')
plt.figtext(0.5, 0.01, 'Units: days', ha='center', fontsize=9, style='italic')
plt.xlim(0, 370)
plt.savefig('images/churn_distribution.png', dpi=150, bbox_inches='tight')
plt.show()


counts = df_churn['classification'].value_counts()

plt.figure(figsize=(8, 6))
sns.barplot(x=counts.index, y=counts.values, hue = counts.index, palette=['#2ecc71', '#f39c12', '#e74c3c'])
plt.title('Customer Churn Segmentation')
plt.xlabel('Segment')
plt.ylabel('Number of Customers')
plt.savefig('images/churn_segmentation.png', dpi=150, bbox_inches='tight')
plt.show()

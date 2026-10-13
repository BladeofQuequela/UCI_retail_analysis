import matplotlib.pyplot as plt
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
import sqlalchemy as sql
import os
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

os.environ['LC_MESSAGES'] = 'C'
os.environ['PGCLIENTENCODING'] = 'UTF8'

from db import engine

df = pd.read_sql('SELECT * FROM survival_gaps_cohorts WHERE duration <= 100', engine)

kmf = KaplanMeierFitter()
kmf.fit(durations=df['duration'], event_observed=df['event'])

plt.figure(figsize=(12, 6))
kmf = KaplanMeierFitter()

for cohort in sorted(df['cohort'].unique()):
    subset = df[df['cohort'] == cohort]
    label = str(cohort)[:7]  # '2010-12'
    kmf.fit(durations=subset['duration'], event_observed=subset['event'], label=label)
    kmf.plot_survival_function(ci_show=False)  # ci_show=False — убираем полосы, иначе будет каша

plt.title('Kaplan-Meier by Cohort: Probability of NOT Returning')
plt.xlabel('Days Since Last Purchase')
plt.ylabel('Survival Probability')
plt.grid(alpha=0.3)
plt.savefig('images/kaplan_meier.png', dpi=150, bbox_inches='tight')
plt.show()

group1 = df[df['cohort'] == '2010-12-01']
group2 = df[df['cohort'] == '2011-02-01']

results = logrank_test(
    durations_A=group1['duration'], event_observed_A=group1['event'],
    durations_B=group2['duration'], event_observed_B=group2['event']
)
print('\n=== Log-rank test: Dec 2010 vs Feb 2011 ===')
print(results.summary)
print(f'\np-value: {results.p_value:.4f}')
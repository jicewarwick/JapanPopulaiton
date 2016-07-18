import pandas as pd
import numpy as np

csv_locale = 'jp.csv'
group_size = 5

data = pd.read_csv(csv_locale, sep='\t', index_col=0)
data.drop('All ages', inplace=True)
data.columns.name = 'year'
age = np.arange(0, 101)
data.index = age
data.index.name = 'age'
year = data.iloc[:, ::3].columns

male = data.iloc[:, 1::3]
male.columns = year
female = data.iloc[:, 2::3]
female.columns = year
total = male + female

male_prop = male.apply(lambda x: x/sum(x))
female_prop = female.apply(lambda x: x/sum(x))
total_prop = total.apply(lambda x: x/sum(x))
total_prop_cum = total_prop.cumsum()

# stack data
male['age'] = male.index
male_melt = pd.melt(male, id_vars='age', value_name='Population')
del male['age']

female['age'] = female.index
female_melt = pd.melt(female, id_vars='age', value_name='Population')
del female['age']

# stats:
# The propotion of people older than 65:
old_prop = 1 - total_prop_cum.iloc[65, ]
old_pop_plot = old_prop.plot(ylim=[0, 0.25], title='Propotion of people above 65 in Japan')
old_pop_plot.get_figure().savefig('old_prop.png')

# segregate data
total_prop['age'] = total_prop.index
total_gp = total_prop.groupby(lambda x: x//group_size)
data = total_gp.sum()
data.index *= group_size
del data['age']
del total_prop['age']

group_density_plot = data.plot().get_figure()
group_density_plot.set_size_inches(12,10)
group_density_plot.savefig('group_density.png')

# highest reproduction rate years:
data.idxmax()

# plot galary

cum_prop_fig = total_prop_cum.plot().get_figure()
cum_prop_fig.set_size_inches(12,10)
cum_prop_fig.savefig('cum_prop.png')


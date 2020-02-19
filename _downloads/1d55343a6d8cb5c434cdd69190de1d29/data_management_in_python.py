"""
Data Management in Python Using Standard Tooling
================================================

Prior to beginning the tutorial, please install the following packages
via ``pip``: - pandas - matplotlib - statsmodels - seaborn - openpyxl -
xlrd

**Note**: if you're using Anaconda, some of these will be installed
already.

**Note**: if you're running the example in Binder, no installation is
necessary

"""


######################################################################
# Overview
# --------
# 


######################################################################
# ``pandas`` is a large library which includes a data structure called a
# ``DataFrame`` which is originally based on R's ``data.frame``. In
# Python, it is built on top of the array datatype in the similarly
# popular ``numpy`` library. Each column in a ``DataFrame`` is a
# ``pandas Series``.
# 
# I use ``numpy`` for some specific functions or when I need higher
# performance than ``pandas``, but ``pandas`` is much more convenient to
# use.
# 
# Here is what we're going to cover:
# 
# -  `**Selecting Data** <#Selecting-Data>`__
# -  `**Aggregating** <#Aggregating>`__
# -  `**Merging** <#Merging>`__
# -  `**Time series** <#Time-series>`__
# -  `**Plotting** <#Plotting>`__
# -  `**Regressions** <#Regressions>`__
# -  `**Input and Output** <#Input-and-Output>`__
# 


######################################################################
# Give me a ``DataFrame``!
# ------------------------
# 
# A ``DataFrame`` can be created in many ways, including: - From a ``csv``
# or Excel file - From a ``SAS7BDAT`` (SAS data) or ``dta`` (Stata data)
# file - From other Python data structures (list of tuples, dictionaries,
# ``numpy`` arrays)
# 


######################################################################
# Here I will create an example ``DataFrame`` from a list of tuples. At
# the end I will show loading and writing to files.
# 

import pandas as pd #this is the convention for importing pandas, then you can use pd. for functions

df = pd.DataFrame(
    data=[
        ('Walmart', 'FL', '1/2/2000', .02),
        ('Walmart', 'FL', '1/3/2000', .03),
        ('Walmart', 'FL', '1/4/2000', .04),
        ('Trader Joes', 'GA', '1/2/2000', .06),
        ('Trader Joes', 'GA', '1/3/2000', .07),
        ('Trader Joes', 'GA', '1/4/2000', .08),
        ('Publix', 'FL', '1/2/2000', .1),
        ('Publix', 'FL', '1/3/2000', .11),
        ('Publix', 'FL', '1/4/2000', .12),
    ], 
    columns = ['Company', 'State', 'Date', 'Return']
)


######################################################################
# ``pandas`` combined with Jupyter gives you a nice representation of your
# data by simply typing the name of the variable storing your
# ``DataFrame``:
# 

df


######################################################################
# Working with Data in Pandas
# ---------------------------
# 


######################################################################
# One of the ``DataFrame``\ s greatest strengths is how flexibly they can
# be split, combined, and aggregated.
# 


######################################################################
# Selecting Data
# ~~~~~~~~~~~~~~
# 

df[df['State'] == 'FL'] # read: dataframe where the dataframe column 'state' is 'FL'

df.iloc[1:3] # give me the second through the third rows

df.iloc[:, 2] # all rows for the third column (looks different because it's a Series)

df['Company'] # company column (Series)

best_grocery_stores = ['Trader Joes', 'Publix']
# only rows where company is in the best grocery stores and has a high return,
# but also give me only the company and return columns
df.loc[df['Company'].isin(best_grocery_stores) & (df['Return'] > 0.07), ['Company', 'Return']] 


######################################################################
# Aggregating
# ~~~~~~~~~~~
# 


######################################################################
# ``DataFrame``\ s have a ``.groupby`` which works similarly to group by
# in a SQL (proc SQL) command.
# 

df.groupby('Company')


######################################################################
# To make it useful, we must aggregate the data somehow:
# 

df.groupby(['State','Date']).mean() #also .median, .std, .count


######################################################################
# Note that there the index becomes the groupby columns. If we want keep
# the columns in the ``DataFrame``, pass ``as_index=False``.
# 

df.groupby(['State','Date'], as_index=False).mean() #also .median, .std, .count


######################################################################
# Note that the shape of the data when using plain groupby is whatever the
# shape of the unique values of the groupby columns. If instead we want to
# add a column to our ``DataFrame`` representing the aggregated values,
# use ``.transform`` on top of ``groupby``.
# 
# This example also shows how to assign a new column to a ``DataFrame``.
# 

df['State Return Average'] = df.groupby(['State','Date']).transform('mean')
df


######################################################################
# Columns can be combined with basic math operations
# 

df['Ratio'] = df['Return'] / df['State Return Average']
df


######################################################################
# Functions can be applied to columns or the entire ``DataFrame``:
# 

import numpy as np # convention for importing numpy.

def sort_ratios(value):

    # If the value is missing or is not a number, return as is
    # Without this, the function will error out as soon as it hits either of those
    if pd.isnull(value) or not isinstance(value, np.float):
        return value
    
    # Otherwise, sort into categories based on the value
    if value == 1:
        return 'Even'
    if value < 1:
        return 'Low'
    if value >= 1:
        return 'High'
    
df['Ratio Size'] = df['Ratio'].apply(sort_ratios) # apply function to ratio column, save result as ratio size column
df

df.applymap(sort_ratios) # apply function to all values in df, but only display and don't save back to df


######################################################################
# Merging
# ~~~~~~~
# 
# See here for more details.
# 


######################################################################
# Let's create a ``DataFrame`` containing information on employment rates
# in the various states and merge it to this dataset.
# 

employment_df = pd.DataFrame(
    data=[
        ('FL', 0.06),
        ('GA', 0.08),
        ('PA', 0.07)
    ],
    columns=['State', 'Unemployment']
)
employment_df

df = df.merge(employment_df, how='left', on='State')
df


######################################################################
# Appending is similarly simple. Here I will append a slightly modified
# ``DataFrame`` to itself:
# 

copy_df = df.copy()
copy_df['Extra Column'] = 5
copy_df.drop('Ratio Size', axis=1, inplace=True) # inplace=True means it gets dropped in the existing DataFrame
df.append(copy_df)


######################################################################
# We can append to the side as well! (concatenate)
# 

temp_df = pd.concat([df, copy_df], axis=1)
temp_df


######################################################################
# Be careful, ``pandas`` allows you to have multiple columns with the same
# name (generally a bad idea):
# 

temp_df['Unemployment']


######################################################################
# Time series
# ~~~~~~~~~~~
# 
# See here for more details.
# 


######################################################################
# Lagging
# ^^^^^^^
# 


######################################################################
# Lags are easy with ``pandas``. The number in shift below represents the
# number of rows to lag.
# 

df.sort_values(['Company', 'Date'], inplace=True)
df['Lag Return'] = df['Return'].shift(1)
df


######################################################################
# But really we want the lagged value to come from the same firm:
# 

df['Lag Return'] = df.groupby('Company')['Return'].shift(1)
df


######################################################################
# Things get slightly more complicated if you want to take into account
# missing dates within a firm. Then you must fill the ``DataFrame`` with
# missing data for those excluded dates, then run the above function, then
# drop those missing rows. A bit too much for this tutorial, but I have
# code available for this upon request.
# 


######################################################################
# Resampling
# ^^^^^^^^^^
# 


######################################################################
# ``pandas`` has a lot of convenient methods for changing the frequency of
# the data.
# 


######################################################################
# Here I will create a df containing intraday returns for the three
# companies
# 

import datetime
from itertools import product

firms = df['Company'].unique().tolist() # list of companies in df
dates = df['Date'].unique().tolist() # list of dates in df
num_periods_per_day = 13 #30 minute intervals
combos = product(firms, dates, [i+1 for i in range(num_periods_per_day)]) # all combinations of company, date, and period number
data_tuples = [
    (
        combo[0], # company
        datetime.datetime.strptime(combo[1], '%m/%d/%Y') + datetime.timedelta(hours=9.5, minutes=30 * combo[2]), #datetime
        np.random.rand() * 100 # price
    ) 
    for combo in combos
]
intraday_df = pd.DataFrame(data_tuples, columns=['Company', 'Datetime', 'Price'])
intraday_df.head() # now the df is quite long, so we can use df.head() and df.tail() to see beginning and end of df


######################################################################
# First must set the date variable as the index to do resampling
# 

intraday_df.set_index('Datetime', inplace=True)


######################################################################
# Now we can resample to aggregate:
# 

intraday_df.groupby('Company').resample('1D').mean()


######################################################################
# Or we can increase the frequency of the data, using ``bfill`` to
# backward fill or ``ffill`` to forward fill. Here I specify to backward
# fill but only go back one period at most.
# 

intraday_df.groupby('Company').resample('10min').bfill(limit=1).head(10)


######################################################################
# Plotting
# ~~~~~~~~
# 


######################################################################
# Oh yeah, we've got graphs too. ``pandas``' plotting functionality is
# built on top of the popular ``matplotlib`` library, which is a graphing
# library based on ``MATLAB``'s graphing functionality.
# 

# we've got to run this magic once per session if we want graphics to show up in the notebook 
# %matplotlib inline


######################################################################
# ``pandas`` tries to guess what you want to plot. By default it will put
# each numeric column as a y variable and the index as the x variable.
# 

df.plot()


######################################################################
# But we can tell it specifically what we want to do. Maybe we want one
# plot for each company showing only how the company return moves relative
# to the state average return over time.
# 

df

df['Date'] = pd.to_datetime(df['Date']) # convert date from string type to datetime type
df.groupby('Company').plot(y=['Return', 'State Return Average'], x='Date')


######################################################################
# ``pandas`` exposes most of the plots in ``matplotlib``. Supported types
# include: - ‘line’ : line plot (default) - ‘bar’ : vertical bar plot -
# ‘barh’ : horizontal bar plot - ‘hist’ : histogram - ‘box’ : boxplot -
# ‘kde’ : Kernel Density Estimation plot - ‘density’ : same as ‘kde’ -
# ‘area’ : area plot - ‘pie’ : pie plot - ‘scatter’ : scatter plot -
# ‘hexbin’ : hexbin plot
# 

df.drop('Ratio', axis=1).plot(kind='box', figsize=(15,8))

df.plot(y=['Return', 'Unemployment'], kind='kde')

market_share_df = pd.DataFrame(
    data=[
        ('Trader Joes', .2),
        ('Walmart', .5),
        ('Publix', .3)
    ],
    columns=['Company', 'Market Share']
).set_index('Company')
market_share_df.plot(y='Market Share', kind='pie', figsize=(6,6))


######################################################################
# Check out the ``seaborn`` package for some cool high level plotting
# capabilities.
# 

import seaborn as sns # convention for importing seaborn
sns.pairplot(df[['Company', 'Return', 'State Return Average']], hue='Company')


######################################################################
# Regressions
# -----------
# 


######################################################################
# Alright, we've got some cleaned up data. Now we can run regressions on
# them with the ``statsmodels`` module. Here I will show the "formula"
# approach to ``statsmodels``, which is just one of the two main
# interfaces. The ``formula`` approach will feel similar to specifying a
# regression in ``R`` or ``Stata``. However we can also directly pass
# ``DataFrames`` containing the y and x variables rather than specifying a
# formula.
# 

df

import statsmodels.formula.api as smf # convention for importing statsmodels

model = smf.ols(formula="Return ~ Unemployment", data=df)
result = model.fit()
result.summary()


######################################################################
# Looks like a regression summary should. We can also use fixed effects
# and interaction terms. Here showing fixed effects:
# 

df.rename(columns={'Ratio Size': 'ratio_size'}, inplace=True) # statsmodels formula doesn't like spaces in column names
model2 = smf.ols(formula="Return ~ Unemployment + C(ratio_size)", data=df)
result2 = model2.fit()
result2.summary()


######################################################################
# Now interaction terms
# 

# use * for interaction keeping individual variables, : for only interaction 
model3 = smf.ols(formula="Return ~ Unemployment*Ratio", data=df) 
result3 = model3.fit()
result3.summary()


######################################################################
# Want to throw together these models into one summary table?
# 

from statsmodels.iolib.summary2 import summary_col

reg_list = [result, result2, result3]
summ = summary_col(
    reg_list,
    stars=True,
    info_dict = {
        'N': lambda x: "{0:d}".format(int(x.nobs)),
        'Adj-R2': lambda x: "{:.2f}".format(x.rsquared_adj)
    }
)
summ


######################################################################
# On the backend, ``statsmodels``' ``summary_col`` uses a ``DataFrame``
# which we can access as:
# 

summ.tables[0]


######################################################################
# Therefore we can write functions to do any cleanup we want on the
# summary, leveraging ``pandas``:
# 

def replace_fixed_effects_cols(df):
    """
    hackish way to do this just for example
    """
    out_df = df.iloc[4:] #remove fixed effect dummy rows
    out_df.loc['Ratio Size Fixed Effects'] = ('No', 'Yes', 'No')
    return out_df

clean_summ = replace_fixed_effects_cols(summ.tables[0])
clean_summ


######################################################################
# Pretty cool, right? Since it's a ``DataFrame``, we can even output it to
# LaTeX:
# 

clean_summ.to_latex()


######################################################################
# Looks messy here, but you can output it to a file. However it's only
# outputting the direct LaTeX for the table so we can add a wrapper so it
# will compile as document:
# 

def _latex_text_wrapper(text):
    begin_text = r"""
    \documentclass[12pt]{article}
\usepackage{booktabs}
\begin{document}

\begin{table}

    """
    
    end_text = r"""
    
    \end{table}
\end{document}
    """
    
    return begin_text + text + end_text

def to_latex(df, filepath='temp.tex'):
    latex = df.to_latex()
    full_latex = _latex_text_wrapper(latex)
    with open(filepath, 'w') as f:
        f.write(full_latex)
        
to_latex(clean_summ) # created temp.tex in this folder. Go look and try to compile


######################################################################
# Input and Output
# ----------------
# 


######################################################################
# Let's output our existing ``DataFrame`` to some different formats and
# then show it can be loaded in through those formats as well.
# 

# We are not using the index, so don't write it to file
df.to_csv('temp.csv', index=False)
df.to_excel('temp.xlsx', index=False)
df.to_stata('temp.dta', write_index=False)
# NOTE: it is possible to read from SAS7BDAT but not write to it

pd.read_csv('temp.csv')

pd.read_excel('temp.xlsx')

pd.read_stata('temp.dta')

# pd.read_sas('temp.sas7bdat') #doesn't exist because we couldn't write to it. But if you already have sas data this will work


######################################################################
# Some Clean Up
# -------------
# 
# This section is not important, just cleaning up the temporary files we
# just generated.
# 

import os

clean_files = [
    'temp.csv',
    'temp.xlsx',
    'temp.dta',
    'temp.tex',
]

for file in clean_files:
    os.remove(file)
import __init__
from init_project import *
#
import sys
import itertools
import statsmodels.api as sm
import pandas as pd
import csv

df2009, df2010 = map(pd.read_csv,
                     [opath.join(dpath['analysis'], 'pickupAP-2009.csv'),
                      opath.join(dpath['analysis'], 'pickupAP-2010.csv')])


df2009.head()
df2009.columns
df2009X = df2009[(df2009['prevEndTerminal'] == 'X')]
df2009O = df2009[(df2009['prevEndTerminal'] != 'X')]

map(len, [df2009X, df2009O])
df2009X['qrTime'].mean()
df2009X[(df2009X['hour'] == 20)]['qrTime'].mean()


df2009O['qrTime'].mean()
df2009O[(df2009O['hour'] == 20)]['qrTime'].mean()

df2009X['hour'].hist()
df2009O['hour'].hist()

df2010X = df2010[(df2010['prevEndTerminal'] == 'X')]
df2010O = df2010[(df2010['prevEndTerminal'] != 'X')]
df2010X['qrTime'].mean()
df2010O['qrTime'].mean()

df2010X['hour'].hist(bins=24)
df2010O['hour'].hist(bins=24)

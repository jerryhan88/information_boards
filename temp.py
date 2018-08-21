import os.path as opath
import os
import pandas as pd
import numpy as np
#
from __path_organizer import adt_dpath

df_200911 = pd.read_csv(opath.join(adt_dpath, 'apDayTrip-20091101.csv'))
df_201001 = pd.read_csv(opath.join(adt_dpath, 'apDayTrip-20100101.csv'))

df = df_200911.append(df_201001)

df_200911.columns
list(map(len, [df_200911, df_201001, df]))

SEC60 = 60


def get_outlierBounds(_data):
    quartile_1, quartile_3 = np.percentile(_data, [25, 75])
    iqr = quartile_3 - quartile_1
    lower_bound = quartile_1 - (iqr * 1.5)
    upper_bound = quartile_3 + (iqr * 1.5)
    return lower_bound, upper_bound


df['interTrip'] = (df['start_time'] - df['time_previous_dropoff']) / SEC60
df['interTrip'].hist()

lower_bound, upper_bound = get_outlierBounds(df['interTrip'])

a = np.where((df['interTrip'] > upper_bound) | (df['interTrip'] < lower_bound))[0]

b = set(df.index).difference(set(a))
df = df.reset_index()
c = set(df.index)
len(c)

adf = df[(df.index.isin(b))]

len(a) / len(df)
len(b)
len(adf) + len(a)

df['duration'] = (df['end_time'] - df['start_time']) / SEC60
lower_bound, upper_bound = get_outlierBounds(df['duration'])
df['duration'].hist()






df['untilFirstFree'] = (df['time_first_free'] - df['time_previous_dropoff']) / SEC60
lower_bound, upper_bound = get_outlierBounds(df['untilFirstFree'])
df['untilFirstFree'].hist()
df[(lower_bound <= df['untilFirstFree']) & (df['untilFirstFree'] <= upper_bound)]['untilFirstFree'].hist()


df['QTime'] = (df['start_time'] - df['time_enter_airport']) / SEC60
lower_bound, upper_bound = get_outlierBounds(df['QTime'])
df['QTime'].hist()



tdf = df[(df['previous_dropoff_loc'] == 'X') & (df['start_loc'] != 'X')]
tdf['QTime'].hist()


tdf['QTime'].mean()


df_strange = df[(df['start_time'] <= df['time_exit_airport'])]
df_strange.head()


df.columns

df.head()

df_200911X = df_200911


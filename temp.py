import os.path as opath
import os
import pandas as pd
#
from __path_organizer import adt_dpath

df_200911 = pd.read_csv(opath.join(adt_dpath, 'apDayTrip-20091101.csv'))
df_201001 = pd.read_csv(opath.join(adt_dpath, 'apDayTrip-20100101.csv'))

df = df_200911.append(df_201001)

df_200911.columns
list(map(len, [df_200911, df_201001, df]))

SEC60 = 60


df['interTrip'] = (df['start_time'] - df['time_previous_dropoff']) / SEC60
df['interTrip'].hist()

df['duration'] = (df['end_time'] - df['start_time']) / SEC60
df['duration'].hist()

df['untilFirstFree'] = (df['time_first_free'] - df['time_previous_dropoff']) / SEC60
df['untilFirstFree'].hist()
df[(df['untilFirstFree'] < 50)]['untilFirstFree'].hist()


df['QTime'] = (df['start_time'] - df['time_enter_airport']) / SEC60
df['QTime'].hist()



tdf = df[(df['previous_dropoff_loc'] == 'X') & (df['start_loc'] != 'X')]
tdf['QTime'].hist()


tdf['QTime'].mean()


df_strange = df[(df['start_time'] <= df['time_exit_airport'])]
df_strange.head()


df.columns

df.head()

df_200911X = df_200911


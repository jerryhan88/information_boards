import os.path as opath
import os
import pandas as pd
import numpy as np
#
from __path_organizer import aggr_dpath

df_2009 = pd.read_csv(opath.join(aggr_dpath, 'apTrip-2009.csv'))
df_2010 = pd.read_csv(opath.join(aggr_dpath, 'apTrip-2010.csv'))




df = df_2009.append(df_2010)
df = df.reset_index()

SEC60 = 60


df['interTrip'] = (df['start_time'] - df['time_previous_dropoff']) / SEC60
df['interTrip'].hist()


df['duration'] = (df['end_time'] - df['start_time']) / SEC60
df['duration'].hist()



df['untilFirstFree'] = (df['time_first_free'] - df['time_previous_dropoff']) / SEC60
df['untilFirstFree'].hist()



df['qeueeing'] = (df['start_time'] - df['time_enter_airport']) / SEC60
df['qeueeing'].hist()


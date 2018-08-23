import os.path as opath
import os
import pandas as pd
import numpy as np
#
from __path_organizer import adt_dpath, aggr_dpath
from __common import WEEKENDS, HOLIDAYS2009, HOLIDAYS2010


def get_outliers(_data):
    quartile_1, quartile_3 = np.percentile(_data, [25, 75])
    iqr = quartile_3 - quartile_1
    lower_bound = quartile_1 - (iqr * 1.5)
    upper_bound = quartile_3 + (iqr * 1.5)
    return np.where((_data > upper_bound) | (_data < lower_bound))[0]


def run(yyyy):
    ofpath = opath.join(aggr_dpath, 'apTrip-%s.csv' % yyyy)
    df = None
    for fn in os.listdir(adt_dpath):
        if not fn.endswith('.csv'):
            continue
        _, yyyymmdd = fn[:-len('.csv')].split('-')
        if not yyyymmdd.startswith(yyyy):
            continue
        fpath = opath.join(adt_dpath, fn)
        df = pd.read_csv(fpath) if df is None else df.append(pd.read_csv(fpath))
    holidays = HOLIDAYS2009 if yyyy == '09' else HOLIDAYS2010
    df['workingDay'] = df.apply(lambda row: 0 if (row['dow'] in WEEKENDS) or
                                                 ((row['year'], row['month'], row['day']) in holidays) else 1,
                                axis=1)
    df = df[(df['workingDay'] == 1)]
    df = df.reset_index()
    #
    df['duration'] = df['end_time'] - df['start_time']
    df['interTrip'] = df['start_time'] - df['time_previous_dropoff']
    df['untilFirstFree'] = df['time_first_free'] - df['time_previous_dropoff']
    df['queueing'] = df['start_time'] - df['time_enter_airport']
    #
    outliers = set()
    for cn in ['duration', 'interTrip', 'untilFirstFree', 'queueing']:
        outliers = outliers.union(set(get_outliers(df[cn])))
    normal_index = set(df.index).difference(outliers)
    filtered_df = df[(df.index.isin(normal_index))]
    filtered_df = filtered_df.drop(['workingDay', 'duration', 'interTrip', 'untilFirstFree', 'queueing'], axis=1)
    filtered_df.to_csv(ofpath, index=False)
    

if __name__ == '__main__':
    run('2009')
    run('2010')
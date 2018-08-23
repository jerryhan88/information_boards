import os.path as opath
import pandas as pd
from datetime import datetime, timedelta
import csv
#
from __path_organizer import aggr_dpath, h2data_dpath


SEC60 = 60

def arrange_datasets():
    yyyys = ['2009', '2010']
    for yyyy in yyyys:
        yyyy = yyyys[0]
        
        ifpath = opath.join(aggr_dpath, 'apTrip-%s.csv' % yyyy)
        df = pd.read_csv(ifpath)   
        df = df[(df['previous_dropoff_loc'] == 'X') & (df['start_loc'] == 'X')]
        df['tMaxFirstFreePrevDropoff'] = df.apply(lambda row: row['time_previous_dropoff'] \
                                                              if row['time_previous_dropoff'] > row['time_first_free'] \
                                                              else row['time_first_free'], axis=1)
        
        df['sunk_cost'] = (df['time_enter_airport'] - df['tMaxFirstFreePrevDropoff']) / SEC60
        
        df['sunk_cost'].hist()
        
        df['time_first_free']
        sunkCost = (eval(row[hid['tPickUp']]) - eval(row[hid['tMaxFirstFreePrevDropoff']])) / MIN1



max(1,2,5,6,7,1)


if __name__ == '__main__':
    arrange_datasets()
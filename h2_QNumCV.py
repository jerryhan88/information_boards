import os.path as opath
import pandas as pd
from datetime import datetime, timedelta
import csv
#
from __path_organizer import aggr_dpath, h2data_dpath
from __common import TERMINALS1, TERMINALS2

AM2, AM6 = 2, 6
TARGET_HOURS1 = list(range(AM6, 24))
TARGET_HOURS2 = list(range(AM2))
INTERVAL_LENGTH = 30  # minutes
REFRESH_INTERVAL = 5  # minutes


def arrange_datasets():
    yyyys = ['2009', '2010']
    for yyyy in yyyys:
        ofpath = opath.join(h2data_dpath, 'apQNum-%s.csv' % yyyy)
        terminals = TERMINALS1[:] if yyyy != '2018' else TERMINALS2[:]
        terminals.pop(terminals.index('X'))
        with open(ofpath, 'w') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_header = ['year', 'month', 'day', 'hour', 'minute']
            new_header += terminals
            writer.writerow(new_header)
        #
        ifpath = opath.join(aggr_dpath, 'apTrip-%s.csv' % yyyy)
        df = pd.read_csv(ifpath)
        df['dt_enter'] = df.apply(lambda row: datetime.fromtimestamp(row['time_enter_airport']), axis=1)
        df['dt_exit'] = df.apply(lambda row: datetime.fromtimestamp(row['time_exit_airport']), axis=1)
        #
        earliest_dt = df['dt_enter'].min()
        latest_dt = df['dt_enter'].max()
        cdt = datetime(earliest_dt.year, earliest_dt.month, earliest_dt.day)        
        while cdt < latest_dt:
            cdf = df[(df['month'] == cdt.month) & (df['day'] == cdt.day) & (df['hour'].isin(TARGET_HOURS1))]
            if len(cdf) == 0:
                cdt += timedelta(days=1)
                continue
            ndt = cdt + timedelta(days=1)
            ndf = df[(df['month'] == ndt.month) & (df['day'] == ndt.day) & (df['hour'].isin(TARGET_HOURS2))]            
            tdf = cdf.append(ndf)
            #
            timer = datetime(cdt.year, cdt.month, cdt.day, AM6)
            lastTime = cdt + timedelta(days=1) + timedelta(hours=AM2)
            while timer < lastTime:
                new_row = [timer.year, timer.month, timer.day, timer.hour, timer.minute]
                tn_numTaxis = []
                tn_df = {tn: tdf[(tdf['start_loc'] == tn)] for tn in terminals}
                for tn in terminals:
                    ter_df = tn_df[tn]
                    num_entered = len(ter_df[(ter_df['dt_enter'] <= timer)])
                    num_exited = len(ter_df[(ter_df['dt_exit'] <= timer)])
                    Qnum = num_entered - num_exited
                    tn_numTaxis.append(Qnum)
                new_row += tn_numTaxis
                with open(ofpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow(new_row)                                
                timer += timedelta(minutes=REFRESH_INTERVAL)
            cdt += timedelta(days=1)


if __name__ == '__main__':
    arrange_datasets()
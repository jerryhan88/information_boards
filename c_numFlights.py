import os.path as opath
import multiprocessing
import os
import pandas as pd
import math
import csv
from datetime import datetime, timedelta
from time import strptime
#
from __path_organizer import ef_dpath, apDF_dpath, apDNF_dpath

AM2, AM6 = 2, 6
REFRESH_INTERVAL = 5  # minutes
INTERVAL_LENGTH = 30  # minutes
TERMINALS = ['T1', 'T2', 'T3', 'T4']


def arrange_numFlightArriaval():
    def process_files(fns, _):
        for fn in fns:
            _, _, yyyymmdd = fn[:-len('.csv')].split('-')
            cur_dt = datetime.strptime(yyyymmdd, '%Y%m%d')
            ofpath = opath.join(apDNF_dpath, 'ap-dayNumFlights-%s.csv' % cur_dt.strftime('%y%m%d'))
            if opath.exists(ofpath):
                continue
            prev_date = cur_dt - timedelta(days=1)
            next_date = cur_dt + timedelta(days=1)
            numDays = 0
            for handling_date in [prev_date, cur_dt, next_date]:
                fpath = opath.join(apDF_dpath, 'ap-dayFlight-%s.csv' % handling_date.strftime('%Y%m%d'))
                if opath.exists(fpath):
                    numDays += 1
                    df = pd.read_csv(fpath) if numDays == 1 else df.append(pd.read_csv(fpath))
            if numDays != 3:
                continue
            with open(ofpath, 'w') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_header = ['year', 'month', 'day', 'hour', 'minute', 'end_interval']
                new_header += TERMINALS
                writer.writerow(new_header)
            #
            df['DateTime'] = df.apply(
                lambda row: datetime(*[row[cn] for cn in ['Year', 'Month', 'Day', 'Hour', 'Minute']]), axis=1)
            inter_begin = datetime(cur_dt.year, cur_dt.month, cur_dt.day, AM6) + timedelta(minutes=0)
            inter_end = datetime(cur_dt.year, cur_dt.month, cur_dt.day, AM6) + timedelta(minutes=INTERVAL_LENGTH)
            last_inter = cur_dt + timedelta(days=1) + timedelta(hours=AM2)
            #
            while inter_begin < last_inter:
                target_df = df[(df['DateTime'] >= inter_begin) & (df['DateTime'] <= inter_end)]
                ndf = target_df.groupby(['Terminal']).count()['DateTime'].reset_index(name='numFlights')
                tn_numFlights = {}
                for tn, numFlights in ndf.values:
                    tn_numFlights[tn] = numFlights
                new_row = [inter_begin.year, inter_begin.month, inter_begin.day,
                           inter_begin.hour, inter_begin.minute,
                           inter_end]
                new_row += [tn_numFlights[tn] if tn in tn_numFlights else 0 for tn in TERMINALS]
                with open(ofpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow(new_row)
                #
                inter_begin += timedelta(minutes=REFRESH_INTERVAL)
                inter_end += timedelta(minutes=REFRESH_INTERVAL)
    #
    numProcessors = multiprocessing.cpu_count()
    worker_fns = [[] for _ in range(numProcessors)]
    for i, fn in enumerate(os.listdir(apDF_dpath)):
        if not fn.endswith('.csv'):
            continue
        worker_fns[i % numProcessors].append(fn)
    ps = []
    for wid, fns in enumerate(worker_fns):
        p = multiprocessing.Process(target=process_files,
                                    args=(fns, wid))
        ps.append(p)
        p.start()
    for p in ps:
        p.join()

    
def arrange_dayFlight():
    for fn in os.listdir(ef_dpath):
        _, _, yyyymmdd = fn[:-len('.csv')].split('-')
        ofpath = opath.join(apDF_dpath, 'ap-dayFlight-%s.csv' % yyyymmdd)
        if opath.exists(ofpath):
            continue
        #
        cur_date = datetime.strptime(yyyymmdd, '%Y%m%d').date()
        #
        df = pd.read_csv(opath.join(ef_dpath, fn))
        if len(df) == 0:
            continue
        df = df[(df['Status'] == 'Landed')]
        df['Updated'] = df.apply(lambda row: row['Updated'] if type(row['Updated']) == float and (not math.isnan(row['Updated'])) \
                                  else row['Scheduled'], axis=1)
        #
        df['Time'] = df.apply(lambda row: row['Updated'][:len('xx:xx')], axis=1)
        df['Date'] = df.apply(lambda row: row['Updated'][len('xx:xx('):-len(')*')], axis=1)
        #
        df['Month'] = df.apply(lambda row: strptime(row['Date'][len('xx '):].capitalize(), '%b').tm_mon \
                      if row['Date'] else cur_date.month, axis=1)
        df['Day'] = df.apply(lambda row: int(row['Date'][:len('xx')]) \
                      if row['Date'] else cur_date.day, axis=1)
        df['Year'] = df.apply(lambda row: cur_date.year + 1 \
                      if cur_date.month == 12 and row['month'] == 1 else cur_date.year, axis=1)
        #
        df['Hour'] = df.apply(lambda row: int(row['Time'][:len('xx')]), axis=1)
        df['Minute'] = df.apply(lambda row: int(row['Time'][len('xx:'):]), axis=1)
        #
        df = df.drop(['Scheduled', 'Updated', 'Time', 'Date', 'Status'], axis=1)
        df = df[['Year', 'Month', 'Day', 'Hour', 'Minute', 'From', 'Flight', 'Terminal', 'Belt']]
        #
        df.to_csv(ofpath, index=False)


if __name__ == '__main__':
    arrange_dayFlight()
    arrange_numFlightArriaval()
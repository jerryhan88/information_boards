import os.path as opath
import multiprocessing
import os
from datetime import datetime, timedelta
import pandas as pd
import csv
#
from __path_organizer import apDT_dpath, apDNT_dpath


AM2, AM6 = 2, 6
REFRESH_INTERVAL = 5  # minutes
INTERVAL_LENGTH = 30  # minutes
TERMINALS = ['T1', 'T2', 'T3', 'B']


def run():
    def process_files(fns, _):
        for fn in fns:
            _, _, yymmdd = fn[:-len('.csv')].split('-')
            cur_dt = datetime.strptime(yymmdd, '%y%m%d')
            ofpath = opath.join(apDNT_dpath, 'ap-dayNumTaxis-%s.csv' % cur_dt.strftime('%Y%m%d'))
            if opath.exists(ofpath):
                continue
            with open(ofpath, 'w') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_header = ['year', 'month', 'day', 'hour', 'minute', 'end_interval']
                new_header += TERMINALS
                writer.writerow(new_header)
            #
            df = pd.read_csv(opath.join(apDT_dpath, fn))
            dt_enters, dt_exits = [], []
            for index, row in df.iterrows():
                pdLoc, sLoc, eLoc = [row[cn] for cn in ['previous_dropoff_loc', 'start_loc', 'end_loc']]
                pdTime, sTime, eTime = [row[cn] for cn in ['time_previous_dropoff', 'start_time', 'end_time']]
                tEnter, tExit = [row[cn] for cn in ['time_enter_airport', 'time_exit_airport']]
                #
                if sLoc != 'X':
                    if pdLoc != 'X':
                        dt_enter = datetime.fromtimestamp(pdTime)
                    else:
                        if tEnter < pdTime:
                            dt_enter = datetime.fromtimestamp(sTime)
                        else:
                            dt_enter = datetime.fromtimestamp(sTime) if sTime < tEnter else datetime.fromtimestamp(
                                tEnter)
                    dt_exit = datetime.fromtimestamp(tExit) if tExit < eTime else datetime.fromtimestamp(eTime)
                else:
                    dt_enter = cur_dt + timedelta(days=1) + timedelta(hours=23)
                    dt_exit = cur_dt + timedelta(days=1) + timedelta(hours=23)
                dt_enters.append(dt_enter)
                dt_exits.append(dt_exit)
            df['dt_enter'] = pd.Series(dt_enters).values
            df['dt_exit'] = pd.Series(dt_exits).values
            #
            inter_begin = datetime(cur_dt.year, cur_dt.month, cur_dt.day, AM6) + timedelta(minutes=0)
            inter_end = datetime(cur_dt.year, cur_dt.month, cur_dt.day, AM6) + timedelta(minutes=INTERVAL_LENGTH)
            last_inter = cur_dt + timedelta(days=1) + timedelta(hours=AM2)
            tn_df = {tn: df[(df['start_loc'] == tn)] for tn in TERMINALS}
            while inter_begin < last_inter:
                tn_numTaxis = []
                for tn in TERMINALS:
                    ter_df = tn_df[tn]
                    qNum = len(ter_df[(ter_df['dt_enter'] <= inter_begin) & (ter_df['dt_exit'] >= inter_end)])
                    tn_numTaxis.append(qNum)
                new_row = [inter_begin.year, inter_begin.month, inter_begin.day,
                           inter_begin.hour, inter_begin.minute,
                           inter_end]
                new_row += tn_numTaxis
                with open(ofpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow(new_row)
                #
                inter_begin += timedelta(minutes=REFRESH_INTERVAL)
                inter_end += timedelta(minutes=REFRESH_INTERVAL)
    #
    numProcessors = multiprocessing.cpu_count()
    worker_fns = [[] for _ in range(numProcessors)]
    for i, fn in enumerate(os.listdir(apDT_dpath)):
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

    
if __name__ == '__main__':
    run()
import os.path as opath
import multiprocessing
import os
from datetime import datetime, timedelta
from bisect import bisect
import csv
#
from util_logging import logging
#
from __path_organizer import lf_dpath, dt_dpath, log_dpath, adt_dpath
#
AM2, AM6 = 2, 6
TARGET_HOURS = list(range(AM6, 24))
TARGET_HOURS += list(range(AM2))
NUM_WORKERS = 7
FREE = 0


def get_target_dates(prefix=None):
    target_date = []
    for fn in os.listdir(dt_dpath):
        if not fn.endswith('.csv'):
            continue
        if prefix and not (prefix in fn):
            continue
        _, yyyymmdd = fn[:-len('.csv')].split('-')
        dt0 = datetime.strptime(yyyymmdd, '%Y%m%d')
        is_valid = True
        for h in TARGET_HOURS:
            if h in [0, 1]:
                next_dt = dt0 + timedelta(days=1)
                dt1 = datetime(next_dt.year, next_dt.month, next_dt.day, h)
            else:
                dt1 = datetime(dt0.year, dt0.month, dt0.day, h)
            fpath = opath.join(log_dpath, 'log-%s.csv' % dt1.strftime('%Y%m%d%H'))
            if not opath.exists(fpath):
                is_valid = False
                break
        if is_valid:
            fpath = opath.join(adt_dpath, 'apDayTrip-%s.csv' % dt0.strftime('%Y%m%d'))
            if opath.exists(fpath):
                continue
            target_date.append(dt0.date())
    #
    return target_date


def process_files(wid, fns, wsDict):
    vid_traj = {}
    for ifpath in fns:
        with open(ifpath) as r_csvfile:
            reader = csv.DictReader(r_csvfile)
            for row in reader:
                vid, state = [int(row[cn]) for cn in ['taxi_id', 'state']]
                t = eval(row['time'])
                loc = row['apBasePos']
                if vid not in vid_traj:
                    vid_traj[vid] = []
                vid_traj[vid].append((t, state, loc))
    wsDict[wid] = vid_traj


def get_trajectory(dt0):
    fns = []
    for h in TARGET_HOURS:
        if h in [0, 1]:
            next_dt = dt0 + timedelta(days=1)
            dt1 = datetime(next_dt.year, next_dt.month, next_dt.day, h)
        else:
            dt1 = datetime(dt0.year, dt0.month, dt0.day, h)


        # if dt1.hour not in [6, 7, 8]:
        #     continue



        fpath = opath.join(log_dpath, 'log-%s.csv' % dt1.strftime('%Y%m%d%H'))
        fns.append(fpath)
    worker_fns = [[] for _ in range(NUM_WORKERS)]
    for i, fn in enumerate(fns):
        worker_fns[i % NUM_WORKERS].append(fn)
    ps = []
    wsDict = multiprocessing.Manager().dict()
    for wid, fns in enumerate(worker_fns):
        p = multiprocessing.Process(target=process_files,
                                    args=(wid, fns, wsDict))
        ps.append(p)
        p.start()
    for p in ps:
        p.join()
    #
    vid_traj0 = {}
    for _, vid_traj1 in wsDict.items():
        for vid, traj1 in vid_traj1.items():
            if vid not in vid_traj0:
                vid_traj0[vid] = []
            vid_traj0[vid] += traj1
    vid_ts = {}
    for vid, traj in vid_traj0.items():
        traj.sort()
        vid_ts[vid] = [t for t, _, _ in traj]
    #
    return vid_ts, vid_traj0


def run(prefix=None):
    logging_fpath = opath.join(lf_dpath, 'a3.txt')
    logging(logging_fpath, 'Start handling')
    target_dates = get_target_dates(prefix)
    #
    for dt in target_dates:
        ofpath = opath.join(adt_dpath, 'apDayTrip-%s.csv' % dt.strftime('%Y%m%d'))
        with open(ofpath, 'w') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_header = [
                'year', 'month', 'day', 'dow', 'hour',
                'taxi_id', 'driver_id', 'fare',
                'previous_dropoff_latitude', 'previous_dropoff_longitude',
                'start_latitude', 'start_longitude',
                'end_latitude', 'end_longitude',
                'previous_dropoff_loc', 'start_loc', 'end_loc',
                'time_previous_dropoff', 'time_enter_airport', 'start_time', 'time_exit_airport', 'end_time',
                'time_first_free']
            writer.writerow(new_header)
        #
        vid_ts, vid_traj0 = get_trajectory(dt)
        ifpath = opath.join(dt_dpath, 'dayTrip-%s.csv' % dt.strftime('%Y%m%d'))
        with open(ifpath) as r_csvfile:
            reader = csv.DictReader(r_csvfile)
            for row in reader:
                vid = int(row['taxi_id'])
                if vid not in vid_ts:
                    continue
                prevLoc, sLoc, eLoc = [row[cn] for cn in ['previous_dropoff_loc', 'start_loc', 'end_loc']]
                tPrev, tStart, tEnd = [eval(row[cn]) for cn in ['time_previous_dropoff', 'start_time', 'end_time']]
                i, j, k = bisect(vid_ts[vid], tPrev), bisect(vid_ts[vid], tStart), bisect(vid_ts[vid], tEnd)
                #
                tEnter, tExit = -1, -1
                if prevLoc == 'X':
                    if sLoc == 'X':
                        for ts, state, loc in vid_traj0[vid][i:j]:
                            if tEnter == -1 and loc != 'X':
                                tEnter = ts
                            if tEnter != -1 and loc == 'X':
                                tExit = ts
                                break
                        else:
                            continue
                    else:
                        for ts, state, loc in vid_traj0[vid][i:j]:
                            if tEnter == -1 and loc != 'X':
                                tEnter = ts
                                break
                        if eLoc == 'X':
                            for ts, state, loc in vid_traj0[vid][j:k]:
                                if tExit == -1 and loc == 'X':
                                    tExit = ts
                                    break
                        else:
                            tExit = tEnd
                else:
                    tEnter = tPrev
                    if sLoc == 'X':
                        for ts, state, loc in vid_traj0[vid][i:j]:
                            if tExit == -1 and loc == 'X':
                                tExit = ts
                                break
                    else:
                        if eLoc == 'X':
                            for ts, state, loc in vid_traj0[vid][j:k]:
                                if tExit == -1 and loc == 'X':
                                    tExit = ts
                                    break
                        else:
                            tExit = tEnd
                if tEnter == -1 or tExit == -1:
                    logging(logging_fpath, 'Cannot find tEnter or tExit; %d, %d\n%s' % (tEnter, tExit, str(row)))
                    continue
                #
                time_ff = -1
                for ts, state, loc in vid_traj0[vid][i:j]:
                    if state == FREE:
                        time_ff = ts
                        break
                if time_ff == -1:
                    logging(logging_fpath, 'Cannot find time_ff; \n%s' % str(row))
                    continue
                #
                new_row = [row[cn] for cn in ['year', 'month', 'day', 'dow', 'hour',
                                        'taxi_id', 'driver_id', 'fare',
                                        'previous_dropoff_latitude', 'previous_dropoff_longitude',
                                        'start_latitude', 'start_longitude',
                                        'end_latitude', 'end_longitude',
                                        'previous_dropoff_loc', 'start_loc', 'end_loc']]
                new_row += [tPrev, tEnter, tStart, tExit, tEnd,
                            time_ff]
                with open(ofpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow(new_row)


if __name__ == '__main__':
    run(prefix='-201001')
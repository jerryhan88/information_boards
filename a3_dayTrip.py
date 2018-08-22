import os.path as opath
import multiprocessing
import os
from datetime import datetime, timedelta
import csv
#
from util_logging import logging
#
from __path_organizer import lf_dpath, trip_dpath, dt_dpath

AM2, AM6 = 2, 6
TARGET_HOURS = list(range(AM6, 24))
TARGET_HOURS += list(range(AM2))
NUM_WORKERS = 8


def get_target_dates(prefix=None):
    _target_days = set()
    for fn in os.listdir(trip_dpath):
        if not fn.endswith('.csv'):
            continue
        if prefix and not (prefix in fn):
            continue
        _, yyyymmddhh = fn[:-len('.csv')].split('-')
        dt = datetime.strptime(yyyymmddhh, '%Y%m%d%H')
        _target_days.add(dt.strftime('%Y%m%d'))
    target_date = []
    for yyyymmdd in _target_days:
        dt0 = datetime.strptime(yyyymmdd, '%Y%m%d')
        is_valid = True
        for h in TARGET_HOURS:
            if h in [0, 1]:
                next_dt = dt0 + timedelta(days=1)
                dt1 = datetime(next_dt.year, next_dt.month, next_dt.day, h)
            else:
                dt1 = datetime(dt0.year, dt0.month, dt0.day, h)
            fpath = opath.join(trip_dpath, 'trip-%s.csv' % dt1.strftime('%Y%m%d%H'))
            if not opath.exists(fpath):
                is_valid = False
                break
        if is_valid:
            fpath = opath.join(dt_dpath, 'dayTrip-%s.csv' % dt0.strftime('%Y%m%d'))
            if opath.exists(fpath):
                continue
            target_date.append(dt0.date())
    #
    return target_date


def process_dates(wid, dts, logging_fpath):
    for dt0 in dts:
        ofpath = opath.join(dt_dpath, 'dayTrip-%s.csv' % dt0.strftime('%Y%m%d'))
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_header = [
                'year', 'month', 'day', 'dow', 'hour',
                'taxi_id', 'driver_id', 'fare',
                'previous_dropoff_longitude', 'previous_dropoff_latitude',
                'start_longitude', 'start_latitude',
                'end_longitude', 'end_latitude',
                'previous_dropoff_loc', 'start_loc', 'end_loc',
                'time_previous_dropoff', 'start_time', 'end_time']
            writer.writerow(new_header)
        #
        vid_lastLocTime, vehicles = {}, {}
        for h in TARGET_HOURS:
            if h in [0, 1]:
                next_dt = dt0 + timedelta(days=1)
                dt1 = datetime(next_dt.year, next_dt.month, next_dt.day, h)
            else:
                dt1 = datetime(dt0.year, dt0.month, dt0.day, h)
            logging(logging_fpath, 'Worker %d: handling %s' % (wid, str(dt1)))
            ifpath = opath.join(trip_dpath, 'trip-%s.csv' % dt1.strftime('%Y%m%d%H'))
            with open(ifpath) as r_csvfile:
                reader = csv.DictReader(r_csvfile)
                for row in reader:
                    vid = int(row['taxi_id'])
                    eLat, eLng, eLoc, eTime = [row[cn] for cn in ['end_latitude', 'end_longitude', 'end_loc', 'end_time']]
                    if not vid in vid_lastLocTime:
                        vid_lastLocTime[vid] = (eLat, eLng, eLoc, eTime)
                        continue
                    latPrevDropoff, lngPrevDropoff, locPrevDropoff, tPrevDropoff = vid_lastLocTime[vid]
                    #
                    new_row = [row[cn] for cn in ['year', 'month', 'day', 'dow', 'hour',
                                                  'taxi_id', 'driver_id', 'fare']]
                    new_row += [latPrevDropoff, lngPrevDropoff]
                    new_row += [row[cn] for cn in ['start_latitude', 'start_longitude',
                                                   'end_latitude', 'end_longitude']]
                    new_row += [locPrevDropoff]
                    new_row += [row[cn] for cn in ['start_loc', 'end_loc']]
                    new_row += [tPrevDropoff]
                    new_row += [row[cn] for cn in ['start_time', 'end_time']]
                    with open(ofpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        writer.writerow(new_row)
                    #
                    vid_lastLocTime[vid] = (eLat, eLng, eLoc, eTime)


def run(prefix=None):
    logging_fpath = opath.join(lf_dpath, 'a3.txt')
    logging(logging_fpath, 'Start handling')
    target_dates = get_target_dates(prefix)
    worker_dts = [[] for _ in range(NUM_WORKERS)]
    for i, dt in enumerate(target_dates):
        worker_dts[i % NUM_WORKERS].append(dt)
    #
    ps = []
    for wid, dts in enumerate(worker_dts):
        p = multiprocessing.Process(target=process_dates,
                                    args=(wid, dts, logging_fpath))
        ps.append(p)
        p.start()
    for p in ps:
        p.join()


if __name__ == '__main__':
    run()

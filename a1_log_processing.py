import os.path as opath
import multiprocessing
import csv
from datetime import datetime, timedelta
from calendar import monthrange
from functools import reduce
#
from util_geoFunctions import get_ap_polygons
from util_logging import logging
#
from __path_organizer import TAXI_RAW_DATA_HOME, lf_dpath, log_dpath

NUM_WORKER = 6


def process_dates(wid, dts, logging_fpath):
    logging(logging_fpath, 'Start worker %d' % wid)
    for ymd_dt in dts:
        logging(logging_fpath, 'Worker %d: handling %s' % (wid, str(ymd_dt)))
        yy, mm = ymd_dt.strftime('%y'), ymd_dt.strftime('%m')
        yyyy = ymd_dt.strftime('%Y')
        #
        log_fpath = reduce(opath.join, [TAXI_RAW_DATA_HOME,
                                        yyyy, mm, 'logs', 'logs-%s-normal.csv' % ymd_dt.strftime('%y%m')])
        ap_polygons = get_ap_polygons()
        next_dt = ymd_dt + timedelta(days=1)
        handling_hour = -1
        with open(log_fpath) as r_csvfile:
            reader = csv.DictReader(r_csvfile)
            for row in reader:
                t, vid, did, state = map(eval, [row[cn] for cn in ['time', 'vehicle-id', 'driver-id', 'state']])
                cur_dt = datetime.fromtimestamp(t)
                if cur_dt.day == next_dt.day:
                    logging(logging_fpath, 'Worker %d: end %s' % (wid, str(ymd_dt)))
                    break
                elif cur_dt.day != ymd_dt.day:
                    continue
                #
                if cur_dt.hour != handling_hour:
                    ofpath = opath.join(log_dpath, 'log-%s.csv' % cur_dt.strftime('%Y%m%d%H'))
                    with open(ofpath, 'w') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        new_header = ['time', 'taxi_id', 'driver_id', 'state', 'lng', 'lat', 'apBasePos']
                        writer.writerow(new_header)
                #
                lng, lat = map(eval, [row[cn] for cn in ['longitude', 'latitude']])
                new_row = [t, vid, did, state, lng, lat]
                apBasePos = 'X'
                for ap_polygon in ap_polygons:
                    if ap_polygon.is_including((lng, lat)):
                        apBasePos = ap_polygon.name
                        break
                new_row.append(apBasePos)
                with open(ofpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow(new_row)


def run(yymm):
    logging_fpath = opath.join(lf_dpath, 'a1_%s.txt' % yymm)
    logging(logging_fpath, 'Start handling; %s' % yymm)
    #
    yymm_dt = datetime.strptime(yymm, '%y%m')
    _, numDays = monthrange(yymm_dt.year, yymm_dt.month)
    first_date = yymm_dt
    last_date = datetime(yymm_dt.year, yymm_dt.month, numDays)
    nm_first_day = last_date + timedelta(days=1)
    handling_date = first_date
    worker_dts = [[] for _ in range(NUM_WORKER)]
    while handling_date < nm_first_day:
        worker_dts[handling_date.day % NUM_WORKER].append(handling_date)
        handling_date += timedelta(days=1)
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
    run('0911')

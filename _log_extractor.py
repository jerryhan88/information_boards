import os.path as opath
import os
import csv
from functools import reduce
from datetime import datetime, timedelta
#
from util_geoFunctions import get_ap_polygons
from util_logging import logging
#
from __path_organizer import TAXI_RAW_DATA_HOME, test_dpath, log_dpath


def extract_from_raw(yymmdd, hh=None, taxi_id=None):
    if type(taxi_id) != int:
        taxi_id = int(taxi_id)
    #
    logging_fpath = opath.join(test_dpath, '_test.txt')
    ofpath = opath.join(test_dpath, 'log-%s-%s-%s.csv' % (yymmdd, hh, taxi_id))
    logging(logging_fpath, 'handle the file; %s' % ofpath)
    with open(ofpath, 'w') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        new_header = ['time', 'taxi_id', 'driver_id', 'state', 'lng', 'lat', 'apBasePos']
        writer.writerow(new_header)
    #
    target_dt = datetime.strptime(yymmdd + hh, '%y%m%d%H')
    next_dt = target_dt + timedelta(hours=1)
    yymm = yymmdd[:len('yymm')]
    yy, mm = yymm[:len('yy')], yymm[len('yy'):]
    yyyy = '20%s' % yy
    #
    log_fpath = reduce(opath.join, [TAXI_RAW_DATA_HOME,
                                    yyyy, mm, 'logs', 'logs-%s-normal.csv' % yymm])
    ap_polygons = get_ap_polygons()
    with open(log_fpath) as r_csvfile:
        reader = csv.DictReader(r_csvfile)
        for row in reader:
            t, vid, did, state = map(eval, [row[cn] for cn in ['time', 'vehicle-id', 'driver-id', 'state']])
            if vid != taxi_id:
                continue
            cur_dt = datetime.fromtimestamp(t)
            if cur_dt.day != target_dt.day:
                continue
            if cur_dt.hour == next_dt.hour:
                logging(logging_fpath, 'next period; %s' % ofpath)
                break
            elif cur_dt.hour != target_dt.hour:
                continue
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


def extract_from_dhLog(yyyymmddhh, taxi_id, returnInstances=False):
    dt = datetime.strptime(yyyymmddhh, '%Y%m%d%H')
    ifpath = opath.join(log_dpath, 'log-%s.csv' % dt.strftime('%Y%m%d%H'))
    #
    if not returnInstances:
        ofpath = opath.join(test_dpath, 'log-%s-%d.csv' % (dt.strftime('%Y%m%d%H'), taxi_id))
        with open(ofpath, 'w') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_header = ['time', 'taxi_id', 'driver_id', 'state', 'lng', 'lat', 'apBasePos']
            writer.writerow(new_header)
        with open(ifpath) as r_csvfile:
            reader = csv.DictReader(r_csvfile)
            for row in reader:
                vid = int(row['taxi_id'])
                if vid != taxi_id:
                    continue
                with open(ofpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow([row[cn] for cn in new_header])
    else:
        rows = []
        with open(ifpath) as r_csvfile:
            reader = csv.DictReader(r_csvfile)
            for row in reader:
                vid = int(row['taxi_id'])
                if vid != taxi_id:
                    continue
                rows.append(row)
        return rows


def extract_by_tripInstance():
    from __path_organizer import viz_dpath
    #
    for fn in os.listdir(viz_dpath):
        if not fn.endswith('trip.csv'):
            continue
        prefix, _ = fn[:-len('.csv')].split('-')
        ofpath = opath.join(viz_dpath, '%s-log.csv' % prefix)
        with open(ofpath, 'w') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_header = ['time', 'taxi_id', 'driver_id', 'state', 'lng', 'lat', 'apBasePos']
            writer.writerow(new_header)
        #
        ifpath = opath.join(viz_dpath, fn)
        with open(ifpath) as r_csvfile:
            reader = csv.DictReader(r_csvfile)
            for row in reader:
                vid = int(row['taxi_id'])
                tPrev, tEnter, tStart, tExit, tEnd = map(eval, [row[cn] for cn in
                                                                ['time_previous_dropoff', 'time_enter_airport',
                                                                 'start_time', 'time_exit_airport', 'end_time']])
        dt_tPrev, dt_tEnter, dt_tStart, dt_tExit, dt_tEnd = map(datetime.fromtimestamp,
                                                                [tPrev, tEnter, tStart, tExit, tEnd])
        #
        rows = []
        handling_dt = dt_tPrev
        while handling_dt < dt_tEnd:
            row = extract_from_dhLog(handling_dt.strftime('%Y%m%d%H'), vid, returnInstances=True)
            rows += row
            handling_dt += timedelta(hours=1)
        for row in rows:
            t = eval(row['time'])
            if t < tPrev:
                continue
            if t > tEnd:
                break
            with open(ofpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow([row[cn] for cn in new_header])


if __name__ == '__main__':
    # extract_from_raw('091101', hh='05', taxi_id=8557)
    # extract_from_dhLog('2009110106', 10995)

    extract_by_tripInstance()

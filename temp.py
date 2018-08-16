import os.path as opath
import os
from datetime import datetime, timedelta
import csv
#
from __path_organizer import viz_dpath
from _log_extractor import extract_from_dhLog



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
            tPrev, tEnter, tStart, tExit, tEnd = map(eval, [row[cn] for cn in ['time_previous_dropoff', 'time_enter_airport', 'start_time', 'time_exit_airport', 'end_time']])
    dt_tPrev, dt_tEnter, dt_tStart, dt_tExit, dt_tEnd = map(datetime.fromtimestamp, [tPrev, tEnter, tStart, tExit, tEnd])
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

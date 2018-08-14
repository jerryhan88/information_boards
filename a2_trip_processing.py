import os.path as opath
import csv
from datetime import datetime
from functools import reduce
#
from util_geoFunctions import get_ap_polygons
from util_logging import logging
#
from __path_organizer import TAXI_RAW_DATA_HOME, lf_dpath, trip_dpath

FREE, ONCALL, POB = 0, 4, 5
MIN20 = 20 * 60


def run(yymm):
    logging_fpath = opath.join(lf_dpath, 'a2_%s.txt' % yymm)
    logging(logging_fpath, 'Start handling; %s' % yymm)
    #
    yymm_dt = datetime.strptime(yymm, '%y%m')
    yy, mm = yymm_dt.strftime('%y'), yymm_dt.strftime('%m')
    yyyy = yymm_dt.strftime('%Y')
    #
    normal_fpath = reduce(opath.join, [TAXI_RAW_DATA_HOME,
                                       yyyy, mm, 'trips', 'trips-%s-normal.csv' % yymm])
    ext_fpath = reduce(opath.join, [TAXI_RAW_DATA_HOME,
                                       yyyy, mm, 'trips', 'trips-%s-normal-ext.csv' % yymm])
    #
    year, month = yymm_dt.year, yymm_dt.month
    ap_polygons = get_ap_polygons()
    handling_day, handling_hour = -1, -1
    with open(normal_fpath) as tripFileN:
        tripReaderN = csv.DictReader(tripFileN)
        with open(ext_fpath) as tripFileE:
            tripReaderE = csv.DictReader(tripFileE)
            for rowN in tripReaderN:
                rowE = next(tripReaderE)
                #
                startTime, endTime = map(eval, [rowN[cn] for cn in ['start-time', 'end-time']])
                cur_dt = datetime.fromtimestamp(startTime)
                if cur_dt.day != handling_day:
                    handling_day = cur_dt.day
                    logging(logging_fpath, 'handle day %d' % handling_day)
                    handling_hour = -1
                if cur_dt.day == handling_day and cur_dt.hour != handling_hour:
                    handling_hour = cur_dt.hour
                    ofpath = opath.join(trip_dpath, 'trip-%s.csv' % cur_dt.strftime('%Y%m%d%H'))
                    with open(ofpath, 'wt') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        new_header = [
                            'year', 'month', 'day', 'dow', 'hour',
                            'taxi_id', 'driver_id', 'fare',
                            'start_latitude', 'start_longitude', 'start_time',
                            'end_latitude', 'end_longitude', 'end_time',
                            'start_loc', 'end_loc',
                        ]
                        writer.writerow(new_header)

                sDay, sDow, sHour = map(int, [rowN[cn] for cn in ['start-day', 'start-dow', 'start-hour']])
                taxiID = int(rowN['vehicle-id'])
                driverID = int(rowE['driver-id'])
                #
                startLng, startLat = map(eval, [rowN[cn] for cn in ['start-long', 'start-lat']])
                endLng, endLat = map(eval, [rowN[cn] for cn in ['end-long', 'end-lat']])
                startLoc, endLoc = 'X', 'X'
                for ap_polygon in ap_polygons:
                    if startLoc == 'X':
                        if ap_polygon.is_including((startLng, startLat)):
                            startLoc = ap_polygon.name
                    if endLoc == 'X':
                        if ap_polygon.is_including((endLng, endLat)):
                            endLoc = ap_polygon.name
                    if startLoc != 'X' and endLoc != 'X':
                        break
                #
                with open(ofpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    new_row = [year, month, sDay, sDow, sHour,
                               taxiID, driverID, rowN['fare'],
                               startLng, startLat, startTime,
                               endLng, endLat, endTime,
                               startLoc, endLoc]
                    writer.writerow(new_row)


if __name__ == '__main__':
    run('0901')

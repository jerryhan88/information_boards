import os.path as opath
import csv
from functools import reduce
from traceback import format_exc
#
from util_geoFunctions import get_ap_polygons, get_ns_polygon
from util_logging import logging
#
from __path_organizer import TAXI_RAW_DATA_HOME, lf_dpath, trip_dpath

FREE, ONCALL, POB = 0, 4, 5
MIN20 = 20 * 60


def run(yymm):
    logging_fpath = opath.join(lf_dpath, 'a2_%s.txt' % yymm)
    ofpath = opath.join(trip_dpath, 'trip-%s.csv' % yymm)
    #
    logging(logging_fpath, 'handle the file; %s' % yymm)
    if opath.exists(ofpath):
        logging(logging_fpath, 'The file had already been processed; %s' % yymm)
        return None
    yy, mm = yymm[:2], yymm[-2:]
    yyyy = '20%s' % yy
    with open(ofpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        new_header = [
            'year', 'month', 'day', 'dow', 'hour',
            'taxi_id', 'driver_id', 'fare',
            'start_latitude', 'start_longitude', 'start_time',
            'end_latitude', 'end_longitude', 'end_time',
            'start_loc', 'end_loc',
            'time_previous_dropoff', 'time_enter_airport', 'time_first_free',
            'loc_previous_dropoff', 'latitude_previous_dropoff', 'longitude_previous_dropoff',
        ]
        writer.writerow(new_header)
    #
    normal_fpath = reduce(opath.join, [TAXI_RAW_DATA_HOME,
                                       yyyy, mm, 'trips', 'trips-%s-normal.csv' % yymm])
    ext_fpath = reduce(opath.join, [TAXI_RAW_DATA_HOME,
                                       yyyy, mm, 'trips', 'trips-%s-normal-ext.csv' % yymm])
    log_fpath = reduce(opath.join, [TAXI_RAW_DATA_HOME,
                                    yyyy, mm, 'logs', 'logs-%s-normal.csv' % yymm])
    handling_day = -1
    try:
        year, month = map(int, [yyyy, mm])
        ap_polygons = get_ap_polygons()
        vehicles = {}
        with open(normal_fpath) as tripFileN:
            tripReaderN = csv.DictReader(tripFileN)
            with open(ext_fpath) as tripFileE:
                tripReaderE = csv.DictReader(tripFileE)
                with open(log_fpath) as logFile:
                    logReader = csv.DictReader(logFile)
                    for rowN in tripReaderN:
                        rowE = next(tripReaderE)
                        sDay, sDow, sHour = map(int, [rowN[cn] for cn in ['start-day', 'start-dow', 'start-hour']])
                        if handling_day != sDay:
                            logging(logging_fpath, 'handle day %d' % sDay)
                            handling_day = sDay
                        #
                        tripTime = eval(rowN['start-time'])
                        while True:
                            rowL = next(logReader)
                            logTime = eval(rowL['time'])
                            vidL, state = map(int, [rowL[cn] for cn in ['vehicle-id', 'state']])
                            if not vehicles.has_key(vidL):
                                vehicles[vidL] = vehicle(vidL, logTime, state)
                            else:
                                vehicles[vidL].update(logTime, state)
                            if tripTime <= logTime:
                                break
                        taxiID = int(rowN['vehicle-id'])
                        if not vehicles.has_key(taxiID):
                            continue
                        driverID = int(rowE['driver-id'])
                        startTime, endTime = map(eval, [rowN[cn] for cn in ['start-time', 'end-time']])
                        timeFirstFree = vehicles[taxiID].firstFreeStateTime
                        vehicles[taxiID].reset()
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
                                       startLoc, endLoc,
                                       timeFirstFree]
                            writer.writerow(new_row)
    except Exception as _:
        logging(logging_fpath, format_exc())
        raise


class vehicle(object):
    def __init__(self, vid, cl_time, cl_state):
        self.vid = vid
        self.pl_time, self.pl_state = cl_time, cl_state
        #
        if self.pl_state == FREE:
            self.firstFreeStateTime = self.pl_time
        else:
            self.firstFreeStateTime = -1
        #
        if self.pl_state == ONCALL:
            self.firstOnCallStateTime = self.pl_time
        else:
            self.firstOnCallStateTime = -1

    def update(self, cl_time, cl_state):
        if cl_state == FREE:
            if self.firstFreeStateTime == -1:
                self.firstFreeStateTime = cl_time
            else:
                if self.pl_state == FREE and MIN20 < cl_time - self.pl_time:
                    self.firstFreeStateTime = cl_time
        elif cl_state == ONCALL:
            if self.firstOnCallStateTime == -1:
                self.firstOnCallStateTime = cl_time
        elif cl_state != POB:
            self.reset()
        else:
            assert cl_state == POB
        #
        self.pl_time, self.pl_state = cl_time, cl_state

    def reset(self):
        self.firstFreeStateTime, self.firstOnCallStateTime = -1, -1


if __name__ == '__main__':
    run('0901')

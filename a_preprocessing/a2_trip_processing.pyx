import __init__
from init_project import *
#
from _utils.logger import get_logger
from _utils.geoFunctions import get_ap_polygons, get_ns_polygon
#
from os.path import expanduser
from datetime import datetime
import csv

logger = get_logger()
TAXI_HOME = expanduser("~") + '/../taxi'

FREE, ONCALL, POB = 0, 4, 5
MIN20 = 20 * 60

def run(yymm):
    from traceback import format_exc
    try:
        logger.info('handle the file; %s' % yymm)
        ofpath = opath.join(dpath['trip'], 'trip-%s.csv' % yymm)
        if opath.exists(ofpath):
            logger.info('The file had already been processed; %s' % yymm)
            return None
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_header = [
                'year', 'month', 'day', 'dow', 'hour',
                'vid', 'did', 'fare',
                'tripType',
                    't0', 't1', 't2', 't3',
                'apBaseStartPos', 'apBaseEndPos',
                'nsBaseStartPos', 'nsBaseEndPos'
            ]
            writer.writerow(new_header)
        yy, mm = yymm[:2], yymm[-2:]
        yyyy = '20%s' % yy
        normal_fpath = opath.join(TAXI_HOME, '%s/%s/trips/trips-%s-normal.csv' % (yyyy, mm, yymm))
        ext_fpath = opath.join(TAXI_HOME, '%s/%s/trips/trips-%s-normal-ext.csv' % (yyyy, mm, yymm))
        log_fpath = opath.join(TAXI_HOME, '%s/%s/logs/logs-%s-normal.csv' % (yyyy, mm, yymm))
        #
        year, month = map(int, [yyyy, mm])
        ap_polygons, ns_polygon = get_ap_polygons(), get_ns_polygon()
        vehicles = {}
        with open(normal_fpath, 'rb') as tripFileN:
            tripReaderN = csv.reader(tripFileN)
            tripHeaderN = tripReaderN.next()
            # {'trip-id': 0, 'job-id': 1, 'start-time': 2, 'end-time': 3,
            #  'start-long': 4, 'start-lat': 5, 'end-long': 6, 'end-lat': 7,
            #  'vehicle-id': 8, 'distance': 9, 'fare': 10, 'duration': 11,
            #  'start-dow': 12, 'start-day': 13, 'start-hour': 14, 'start-minute': 15,
            #  'end-dow': 16, 'end-day': 17, 'end-hour': 18, 'end-minute': 19}
            hidN = {h: i for i, h in enumerate(tripHeaderN)}
            with open(ext_fpath, 'rb') as tripHeaderE:
                tripReaderE = csv.reader(tripHeaderE)
                tripHeaderE = tripReaderE.next()
                # {'start-zone': 0, 'end-zone': 1, 'start-postal': 2, 'end-postal': 3,
                # 'driver-id': 4, 'trip-type': 5}
                hidE = {h: i for i, h in enumerate(tripHeaderE)}
                with open(log_fpath, 'rb') as logFile:
                    logReader = csv.reader(logFile)
                    logHeader = logReader.next()
                    hidL = {h: i for i, h in enumerate(logHeader)}
                    for rowN in tripReaderN:
                        rowE = tripReaderE.next()
                        #
                        tripTime = eval(rowN[hidN['start-time']])
                        while True:
                            rowL = logReader.next()
                            logTime = eval(rowL[hidL['time']])
                            vidL, state = map(int, [rowL[hidL[cn]] for cn in ['vehicle-id', 'state']])
                            if not vehicles.has_key(vidL):
                                vehicles[vidL] = vehicle(vidL, logTime, state)
                            else:
                                vehicles[vidL].update(logTime, state)
                            if tripTime <= logTime:
                                break
                        vidT = int(rowN[hidN['vehicle-id']])
                        if not vehicles.has_key(vidT):
                            continue
                        didT = int(rowE[hidE['driver-id']])
                        tripType = int(rowE[hidE['trip-type']])
                        t2, t3 = map(eval, [rowN[hidN[cn]] for cn in ['start-time', 'end-time']])
                        t0 = vehicles[vidT].firstFreeStateTime
                        if t0 == -1:
                            continue
                        t1 = vehicles[vidT].firstOnCallStateTime if tripType else t2
                        vehicles[vidT].reset()
                        #
                        startLon, startLat = map(eval, [rowN[hidN[cn]] for cn in ['start-long', 'start-lat']])
                        endLon, endLat = map(eval, [rowN[hidN[cn]] for cn in ['end-long', 'end-lat']])
                        apBaseStartPos, apBaseEndPos = 'X', 'X'
                        for ap_polygon in ap_polygons:
                            if apBaseStartPos == 'X':
                                if ap_polygon.is_including((startLon, startLat)):
                                    apBaseStartPos = ap_polygon.name
                            if apBaseEndPos == 'X':
                                if ap_polygon.is_including((endLon, endLat)):
                                    apBaseEndPos = ap_polygon.name
                            if apBaseStartPos != 'X' and apBaseEndPos != 'X':
                                break
                        nsBaseStartPos = 'O' if ns_polygon.is_including((startLon, startLat)) else 'X'
                        nsBaseEndPos = 'O' if ns_polygon.is_including((endLon, endLat)) else 'X'
                        #
                        with open(ofpath, 'a') as w_csvfile:
                            writer = csv.writer(w_csvfile, lineterminator='\n')
                            new_row = [year, month]
                            new_row += [rowN[hidN[cn]] for cn in ['start-day', 'start-dow', 'start-hour']]
                            new_row += [vidT, didT]
                            new_row += [rowN[hidN['fare']]]
                            new_row += [tripType, t0, t1, t2, t3]
                            new_row += [apBaseStartPos, apBaseEndPos, nsBaseStartPos, nsBaseEndPos]
                            writer.writerow(new_row)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
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

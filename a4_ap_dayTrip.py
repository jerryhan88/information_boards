import os.path as opath
from bisect import bisect
import csv
from traceback import format_exc
#
from util_logging import logging
#
from __path_organizer import lf_dpath, trip_dpath, apDL_dpath, apDT_dpath

AM2, AM5 = 2, 5


def run(yymm):
    logging_fpath = opath.join(lf_dpath, 'a4_%s.txt' % yymm)
    #
    logging(logging_fpath, 'handle the file; %s' % yymm)
    trip_fpath = opath.join(trip_dpath, 'trip-%s.csv' % yymm)
    handling_day = 0
    vid_lastLocTime, vehicles = {}, {}
    try:
        with open(trip_fpath) as tripFile:
            tripReader = csv.DictReader(tripFile)
            for row in tripReader:
                did = int(row['driver_id'])
                if did == -1:
                    continue
                day, hour = map(int, [row[cn] for cn in ['day', 'hour']])
                if day == 1 and hour <= AM5:
                    continue
                if AM2 <= hour and hour <= AM5:
                    continue
                if day != handling_day and hour == AM5 + 1:
                    handling_day = day
                    logging(logging_fpath, 'handling %dth day' % handling_day)
                    vid_lastLocTime, vehicles = {}, {}
                    log_fpath = opath.join(apDL_dpath, 'ap-dayLog-%s%02d.csv' % (yymm, handling_day))
                    with open(log_fpath) as logFile:
                        logReader = csv.DictReader(logFile)
                        for rowL in logReader:
                            vid = int(rowL['driver_id'])
                            if not vid in vehicles:
                                vehicles[vid] = vehicle(vid)
                            vehicles[vid].add_trajectory(eval(rowL['time']), rowL['apBasePos'])
                    #
                    ofpath = opath.join(apDT_dpath, 'ap-dayTrip-%s%02d.csv' % (yymm, handling_day))
                    with open(ofpath, 'wt') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        new_header = [
                            'year', 'month', 'day', 'dow', 'hour',
                            'taxi_id', 'driver_id', 'fare',
                            'start_latitude', 'start_longitude', 'start_time',
                            'end_latitude', 'end_longitude', 'end_time',
                            'start_loc', 'end_loc',
                            'time_first_free', 'time_previous_dropoff', 'time_enter_airport', 'time_exit_airport',
                            'previous_dropoff_latitude', 'previous_dropoff_longitude', 'previous_dropoff_loc',
                        ]
                        writer.writerow(new_header)
                vid = int(row['taxi_id'])
                if not vid in vehicles:
                    continue
                sLoc, eLoc = [row[cn] for cn in ['start_loc', 'end_loc']]
                sTime, eTime = map(eval, [row[cn] for cn in ['start_time', 'end_time']])
                eLat, eLng = map(eval, [row[cn] for cn in ['end_latitude', 'end_longitude']])
                if not vid in vid_lastLocTime:
                    vid_lastLocTime[vid] = (eLat, eLng, eLoc, eTime)
                    continue
                latPrevDropoff, lngPrevDropoff, locPrevDropoff, tPrevDropoff = vid_lastLocTime[vid]
                if not (locPrevDropoff == 'X' and sLoc == 'X'):
                    tEnter, tExit = vehicles[vid].find_eeTime_AP(sTime, sLoc)
                    newInfo = [tPrevDropoff, tEnter, tExit,
                               latPrevDropoff, lngPrevDropoff, locPrevDropoff]
                    add_row(ofpath, row, newInfo)
                else:
                    visitAP, tEnter, tExit = vehicles[vid].find_eeTime_XAP(tPrevDropoff, sTime)
                    if visitAP:
                        newInfo = [tPrevDropoff, tEnter, tExit,
                                   latPrevDropoff, lngPrevDropoff, locPrevDropoff]
                        add_row(ofpath, row, newInfo)
                vid_lastLocTime[vid] = (eLoc, eTime)
    except Exception as _:
        logging(logging_fpath, format_exc())
        raise


def add_row(ofpath, row, newInfo):
    with open(ofpath, 'a') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        new_row = [row[cn] for cn in ['year', 'month', 'day', 'dow', 'hour',
                                      'taxi_id', 'driver_id', 'fare',
                                      'start_latitude', 'start_longitude', 'start_time',
                                      'end_latitude', 'end_longitude', 'end_time',
                                      'start_loc', 'end_loc',
                                      'time_first_free']]
        new_row += newInfo
        writer.writerow(new_row)


class vehicle(object):
    def __init__(self, vid):
        self.vid = vid
        self.tra_time, self.tra_loc = [], []

    def add_trajectory(self, t, loc):
        self.tra_time.append(t)
        self.tra_loc.append(loc)

    def find_eeTime_AP(self, pickupTime, pickUpTerminal):
        i = bisect(self.tra_time, pickupTime)
        if i == len(self.tra_loc):
            entering_time, exiting_time = self.tra_time[i - 1], 1e400
        else:
            loc0, loc1 = self.tra_loc[i - 1], self.tra_loc[i]
            if loc0 == pickUpTerminal:
                entering_time, exiting_time = self.tra_time[i - 1], self.tra_time[i]
            elif loc1 == pickUpTerminal:
                if i + 1 == len(self.tra_loc):
                    entering_time, exiting_time = self.tra_time[i], 1e400
                else:
                    entering_time, exiting_time = self.tra_time[i], self.tra_time[i + 1]
            else:
                entering_time, exiting_time = 1e400, 1e400
        return entering_time, exiting_time

    def find_eeTime_XAP(self, tPrevDropoff, tPickUp):
        i, j = [bisect(self.tra_time, t) for t in [tPrevDropoff, tPickUp]]
        tEnter, tExit = None, None
        if i == len(self.tra_loc):
            visitAP = False
            return visitAP, tEnter, tExit
        else:
            for k in range(i, j):
                loc = self.tra_loc[k]
                if tEnter == None and loc != 'X':
                    tEnter = self.tra_time[k]
                if tEnter != None and loc == 'X':
                    tExit = self.tra_time[k]
                    visitAP = True
                    break
            else:
                visitAP = False
            return visitAP, tEnter, tExit


if __name__ == '__main__':
    run('0901')

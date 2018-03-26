import sys, os
import os.path as opath
from datetime import datetime
from bisect import bisect
import csv

AM2, AM5 = 2, 5


def run(trip_fpath, trip_dir, log_dir):
    handling_day = 0
    vid_lastLocTime, vehicles = {}, {}
    dayLogs = {}
    with open(trip_fpath) as r_csvfileTrip:
        tirpReader = csv.DictReader(r_csvfileTrip)
        for rowT in tirpReader:
            tPickUp = eval(rowT['tPickUp'])
            pu_dt = datetime.fromtimestamp(tPickUp)
            day, hour = pu_dt.day, pu_dt.hour
            if day == 1 and hour <= AM5:
                continue
            if AM2 <= hour and hour <= AM5:
                continue
            if day != handling_day and hour == AM5 + 1:
                handling_day = day
                if (day, hour) not in dayLogs:
                    vid_lastLocTime, vehicles = {}, {}
                    log_fpath = opath.join(log_dir,
                               'dayLog-%d%02d%02d.csv' % ((pu_dt.year - 2000), pu_dt.month, handling_day))
                    with open(log_fpath) as r_csvfileLog:
                        logReader = csv.DictReader(r_csvfileLog)
                        for rowL in logReader:
                            vid = rowL['vid']
                            if vid not in vehicles:
                                vehicles[vid] = vehicle(vid)
                            vehicles[vid].add_trajectory(eval(rowL['time']), rowL['apBasePos'])
                    dayLogs[day, hour] = [vid_lastLocTime, vehicles]
                else:
                    vid_lastLocTime, vehicles = dayLogs[day, hour]
                #
                ofpath = opath.join(trip_dir,
                        'dayTrip-%d%02d%02d.csv' % ((pu_dt.year - 2000), pu_dt.month, handling_day))
                if not opath.exists(ofpath):
                    with open(ofpath, 'wt') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        new_headers = [
                            'year', 'month', 'day', 'dow', 'hour',
                            'fare',
                            'locPrevDropoff', 'locPickup', 'locDropoff',
                            'tPrevDropoff', 'tEnter', 'tExit',
                            'tripType',
                                'tPickUp', 'tDropOff']
                        writer.writerow(new_headers)
            vid = rowT['vid']
            if vid not in vehicles:
                continue
            locPickup, locDropoff = [rowT[cn] for cn in ['apBaseStartPos', 'apBaseEndPos']]
            tPickUp, tDropOff = map(eval, [rowT[cn] for cn in ['tPickUp', 'tDropOff']])
            if vid not in vid_lastLocTime:
                vid_lastLocTime[vid] = (locDropoff, tDropOff)
                continue
            locPrevDropoff, tPrevDropoff = vid_lastLocTime[vid]
            if not (locPrevDropoff == 'X' and locPickup == 'X'):
                tEnter, tExit = vehicles[vid].find_eeTime_AP(tPickUp, locPickup)
                others = [locPrevDropoff, locPickup, locDropoff, tPrevDropoff, tEnter, tExit]
                add_row(ofpath, rowT, pu_dt, others)
            else:
                visitAP, tEnter, tExit = vehicles[vid].find_eeTime_XAP(tPrevDropoff, tPickUp)
                others = [locPrevDropoff, locPickup, locDropoff, tPrevDropoff, tEnter, tExit]
                if visitAP:
                    add_row(ofpath, rowT, pu_dt, others)
            vid_lastLocTime[vid] = (locDropoff, tDropOff)


def add_row(ofpath, row, pu_dt, others):
    year, month, day = pu_dt.year, pu_dt.month, pu_dt.day
    dow, hour = pu_dt.weekday(), pu_dt.hour
    locPrevDropoff, locPickup, locDropoff, tPrevDropoff, tEnter, tExit = others
    with open(ofpath, 'a') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        new_row = [year, month, day, dow, hour]
        new_row += [row['fare']]
        new_row += [locPrevDropoff, locPickup, locDropoff]
        new_row += [tPrevDropoff, tEnter, tExit]
        new_row += [row[cn] for cn in ['tripType',
                                             'tPickUp', 'tDropOff']]
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
    if len(sys.argv) == 3:
        trip_fpath, trip_dir, log_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    else:
        trip_fpath = 'trip_out.csv'
        trip_dir = os.getcwd()
        log_dir = os.getcwd()

    run(trip_fpath, trip_dir, log_dir)
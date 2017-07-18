import __init__
from init_project import *
#
from _utils.logger import get_logger
#
from bisect import bisect
import csv

logger = get_logger()


def run(yymm):
    from traceback import format_exc
    try:
        logger.info('handle the file; %s' % yymm)
        trip_fpath = opath.join(dpath['trip'], 'trip-%s.csv' % yymm)
        handling_day = 0
        vid_lastLocTime, vehicles = {}, {}
        with open(trip_fpath, 'rb') as tripFile:
            tripReader = csv.reader(tripFile)
            tripHeader = tripReader.next()
            hidT = {h: i for i, h in enumerate(tripHeader)}
            for row in tripReader:
                did = int(row[hidT['did']])
                if did == -1:
                    continue
                day, hour = map(int, [row[hidT[cn]] for cn in ['day', 'hour']])
                if day == 1 and hour <= AM5:
                    continue
                if AM2 <= hour and hour <= AM5:
                    continue
                if day != handling_day and hour == AM5 + 1:
                    handling_day = day
                    vid_lastLocTime, vehicles = {}, {}
                    log_fpath = opath.join(dpath['ap_dayLog'], 'ap-dayLog-%s%02d.csv' % (yymm, handling_day))
                    with open(log_fpath, 'rb') as logFile:
                        logReader = csv.reader(logFile)
                        logHeader = logReader.next()
                        hidL = {h: i for i, h in enumerate(logHeader)}
                        for rowL in logReader:
                            vid = int(rowL[hidL['vid']])
                            if not vehicles.has_key(vid):
                                vehicles[vid] = vehicle(vid)
                            vehicles[vid].add_trajectory(eval(rowL[hidL['time']]), rowL[hidL['apBasePos']])
                    #
                    ofpath = opath.join(dpath['ap_dayTrip'], 'ap-dayTrip-%s%02d.csv' % (yymm, handling_day))
                    with open(ofpath, 'wt') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        new_headers = [
                            'year', 'month', 'day', 'dow', 'hour',
                            'did', 'fare',
                            'locPrevDropoff', 'locPickup', 'locDropoff',
                            'tPrevDropoff', 'tEnter', 'tExit',
                            'tripType',
                                'tFirstFree', 'tFirstOnCall', 'tPickUp', 'tDropOff']
                        writer.writerow(new_headers)
                vid = int(row[hidT['vid']])
                locPickup, locDropoff = [row[hidT[cn]] for cn in ['apBaseStartPos', 'apBaseEndPos']]
                tPickUp, tDropOff = map(eval, [row[hidT[cn]] for cn in ['tPickUp', 'tDropOff']])
                if not vid_lastLocTime.has_key(vid):
                    vid_lastLocTime[vid] = (locDropoff, tDropOff)
                    continue
                locPrevDropoff, tPrevDropoff = vid_lastLocTime[vid]
                if not (locPrevDropoff == 'X' and locPickup == 'X'):
                    if not vehicles.has_key(vid):
                        continue
                    tEnter, tExit = vehicles[vid].find_eeTime(tPickUp, locPickup)
                    with open(ofpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        new_row = [row[hidT[cn]] for cn in ['year', 'month', 'day', 'dow', 'hour',
                                                            'did', 'fare']]
                        new_row += [locPrevDropoff, locPickup, locDropoff]
                        new_row += [tPrevDropoff, tEnter, tExit]
                        new_row += [row[hidT[cn]] for cn in ['tripType',
                                                                'tFirstFree', 'tFirstOnCall', 'tPickUp', 'tDropOff']]
                        writer.writerow(new_row)
                vid_lastLocTime[vid] = (locDropoff, tDropOff)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise


class vehicle(object):
    def __init__(self, vid):
        self.vid = vid
        self.tra_time, self.tra_loc = [], []

    def add_trajectory(self, t, loc):
        self.tra_time.append(t)
        self.tra_loc.append(loc)

    def find_eeTime(self, pickupTime, pickUpTerminal):
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


if __name__ == '__main__':
    run('0901')

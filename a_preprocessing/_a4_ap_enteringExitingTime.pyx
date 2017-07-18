import __init__
from init_project import *
#
from traceback import format_exc
from bisect import bisect
from fnmatch import fnmatch
import csv


def run(yymm):
    for fn in os.listdir(dpath['trip_ap']):
        if not fnmatch(fn, 'trip-ap-%s*.csv' % yymm):
            continue
        _, _, yymmdd = fn[:-len('.csv')].split('-')
        process_daily(yymmdd)


def run_multiple_cores(processorID, numWorkers=11):
    for i, fn in enumerate(os.listdir(dpath['trip_ap'])):
        if not fnmatch(fn, 'trip-ap-*.csv'):
            continue
        if i % numWorkers != processorID:
            continue
        _, _, yymmdd = fn[:-len('.csv')].split('-')
        process_daily(yymmdd)


def process_daily(yymmdd):
    log_fpath = opath.join(dpath['log_ap'], 'log-ap-%s.csv' % yymmdd)
    trip_fpath = opath.join(dpath['trip_ap'], 'trip-ap-%s.csv' % yymmdd)

    try:
        ofpath = opath.join(dpath['eeTime_ap'], 'eeTime-ap-%s.csv' % yymmdd)
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_header = ['vid', 'did',
                           'pickupTime', 'dropoffTime', 'duration', 'fare',
                           'enteringTime', 'exitingTime',
                           'pickUpTerminal',
                           'prevEndTerminal', 'prevTripEndTime',
                           'year', 'month', 'day', 'hour', 'dow']
            writer.writerow(new_header)
        #
        vehicles = {}
        with open(log_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                t = eval(row[hid['time']])
                vid = int(row[hid['vid']])
                apBasePos = row[hid['apBasePos']]
                if not vehicles.has_key(vid):
                    vehicles[vid] = vehicle(vid)
                vehicles[vid].add_trajectory(t, apBasePos)
        #
        with open(trip_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                prevEndTerminal, pickUpTerminal = (row[hid[cn]] for cn in ['prevEndTerminal', 'pickUpTerminal'])
                if prevEndTerminal == 'X' and pickUpTerminal == 'X':
                    continue
                vid = int(row[hid['vid']])
                startTime = eval(row[hid['startTime']])
                if not vehicles.has_key(vid):
                    continue
                enteringTime, exitingTime = vehicles[vid].find_eeTime(startTime, pickUpTerminal)
                new_row = [row[hid[cn]] for cn in ['vid', 'did',
                                                   'startTime', 'endTime', 'duration', 'fare']]
                new_row += [enteringTime, exitingTime]
                new_row += [row[hid[cn]] for cn in ['pickUpTerminal',
                                                    'prevEndTerminal', 'prevTripEndTime',
                                                    'year', 'month', 'day', 'hour', 'dow']]
                with open(ofpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow(new_row)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymmdd), 'w') as f:
            f.write(format_exc())
        raise


class vehicle(object):
    def __init__(self, vid):
        self.vid = vid
        self.tra_time, self.tra_loc = [], []

    def update_trajectory(self, t, loc):
        self.tra_time += [t]
        self.tra_loc += [loc]

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
                    entering_time, exiting_time = self.tra_time[i],  self.tra_time[i + 1]
            else:
                entering_time, exiting_time = 1e400, 1e400
        return entering_time, exiting_time


if __name__ == '__main__':
    pass

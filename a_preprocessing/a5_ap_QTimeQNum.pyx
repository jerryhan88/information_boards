import __init__
from init_project import *
#
from traceback import format_exc
from fnmatch import fnmatch
from datetime import datetime
import pandas as pd
import csv


def run(yymm):
    for fn in os.listdir(dpath['ap_dayTrip']):
        if not fnmatch(fn, 'ap-dayTrip-%s*.csv' % yymm):
            continue
        _, _, yymmdd = fn[:-len('.csv')].split('-')
        process_daily(yymmdd)


def process_daily(yymmdd):
    ifpath = opath.join(dpath['ap_dayTrip'], 'ap-dayTrip-%s.csv' % yymmdd)
    ofpath = opath.join(dpath['ap_QTimeQNum'], 'ap-QTimeQNum-%s.csv' % yymmdd)
    try:
        df = pd.read_csv(ifpath)
        terminals = [ter for ter in set(df['locPrevDropoff']) if ter != 'X']
        terminals.sort()
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_header = [
                'year', 'month', 'day', 'dow', 'hour',
                'did', 'fare',
                'locPrevDropoff', 'locPickup', 'locDropoff',
                'tPrevDropoff', 'tEnter', 'tExit',
                'tripType',
                'tFirstFree', 'tFirstOnCall', 'tPickUp', 'tDropOff'
                ]
            new_header += ['QTime']
            new_header += terminals
            writer.writerow(new_header)
        #
        with open(ifpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                locPrevDropoff, locPickup = [row[hid[cn]] for cn in ['locPrevDropoff', 'locPickup']]
                tPrevDropoff, tPickUp = map(eval, [row[hid[cn]] for cn in ['tPrevDropoff', 'tPickUp']])
                if locPickup == 'X':  # Case 1
                    QTime = -1
                else:
                    if locPrevDropoff == locPickup:  # Case 2
                        QTime = -2
                    else:
                        if row[hid['tEnter']] == 'inf':  # Case 3
                            QTime = -3
                        else:
                            tEnter = eval(row[hid['tEnter']])
                            if tPickUp < tEnter:  # Case 4
                                QTime = -4
                            else:
                                QTime = tPickUp - tEnter
                new_row = [row[hid[cn]] for cn in [
                                                    'year', 'month', 'day', 'dow', 'hour',
                                                    'did', 'fare',
                                                    'locPrevDropoff', 'locPickup', 'locDropoff',
                                                    'tPrevDropoff', 'tEnter', 'tExit',
                                                    'tripType',
                                                    'tFirstFree', 'tFirstOnCall', 'tPickUp', 'tDropOff']]
                new_row += [QTime]
                for ter in terminals:
                    ter_df = df[(df['locPickup'] == ter)]
                    num_entered = len(ter_df[(ter_df['tEnter'] <= tPrevDropoff)])
                    num_exited = len(ter_df[(ter_df['tExit'] <= tPrevDropoff)])
                    QNum = num_entered - num_exited
                    new_row += [QNum]
                with open(ofpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow(new_row)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymmdd), 'w') as f:
            f.write(format_exc())
        raise


def filtering(yy):
    filtered_fpath = opath.join(dpath['qrTimeTerNumber_ap'], 'Filtered-qrTimeTerNumber-ap-20%s.csv' % yy)
    with open(filtered_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        new_header = [
            'did',
            'prevEndTerminal', 'prevTripEndTime',
                'T1', 'T2', 'T3', 'BudgetT',
            'pickUpTerminal',
                'enteringTime', 'pickupTime', 'exitingTime',
            'dropoffTime',
            'year', 'month', 'day', 'hour', 'weekEnd',
            'duration', 'fare',
            'qrTime', 'productivity'
        ]
        writer.writerow(new_header)
    #
    summary_fpath = opath.join(dpath['analysis'], 'whole-ap-20%s.csv' % yy)
    holidays = HOLIDAYS2009 if yy == '09' else HOLIDAYS2010
    with open(summary_fpath, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        header = reader.next()
        hid = {h: i for i, h in enumerate(header)}
        for row in reader:
            qrTime, productivity, duration, fare = map(eval, [row[hid[cn]] for cn in
                                                              ['qrTime', 'productivity', 'duration', 'fare']])
            if qrTime <= TH_QRTIME_MIN or qrTime > TH_QRTIME_MAX:
                continue
            if productivity > TH_PRODUCTIVITY:
                continue
            if duration <= TH_DURATION:
                continue
            enteringTime = 0 if row[hid['enteringTime']] == 'inf' else eval(row[hid['enteringTime']])
            pickupTime = eval(row[hid['pickupTime']])
            exitingTime = 1e400 if row[hid['exitingTime']] == 'inf' else eval(row[hid['exitingTime']])
            if pickupTime < enteringTime or exitingTime < pickupTime:
                continue
            #
            year, month, day, hour = map(int, [row[hid[cn]] for cn in ['year', 'month', 'day', 'hour']])
            weekEnd = 0
            if (year, month, day) in holidays:
                weekEnd = 1
            if datetime(year, month, day).weekday() in WEEKENDS:
                weekEnd = 1
            #
            new_row = [row[hid[cn]] for cn in ['did',
                                               'prevEndTerminal', 'prevTripEndTime',
                                                    'T1', 'T2', 'T3', 'BudgetT',
                                               'pickUpTerminal',
                                                    'enteringTime', 'pickupTime', 'exitingTime',
                                               'dropoffTime']]
            new_row += [year, month, day, hour, weekEnd]
            new_row += [duration, fare]
            new_row += [qrTime, productivity]
            with open(filtered_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow(new_row)


if __name__ == '__main__':
    # filtering('09')
    filtering('10')

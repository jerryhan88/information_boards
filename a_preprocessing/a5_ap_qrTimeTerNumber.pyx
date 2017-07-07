import __init__
from init_project import *
#
from traceback import format_exc
from fnmatch import fnmatch
from datetime import datetime
import pandas as pd
import csv


def run(yymm):
    for fn in os.listdir(dpath['eeTime_ap']):
        if not fnmatch(fn, 'eeTime-ap-%s*.csv' % yymm):
            continue
        _, _, yymmdd = fn[:-len('.csv')].split('-')
        process_daily(yymmdd)



def run_multiple_cores(processorID, numWorkers=11):
    for i, fn in enumerate(os.listdir(dpath['eeTime_ap'])):
        if not fnmatch(fn, 'eeTime-ap-*.csv'):
            continue
        if i % numWorkers != processorID:
            continue
        _, _, yymmdd = fn[:-len('.csv')].split('-')
        process_daily(yymmdd)



def process_daily(yymmdd):
    ifpath = opath.join(dpath['eeTime_ap'], 'eeTime-ap-%s.csv' % yymmdd)
    try:
        df = pd.read_csv(ifpath)
        terminals = [ter for ter in set(df['pickUpTerminal']).union(set(df['prevEndTerminal'])) if ter != 'X']
        ofpath = opath.join(dpath['qrTimeTerNumber_ap'], 'qrTimeTerNumber-ap-%s.csv' % yymmdd)
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_headers = ['did',
                           'pickupTime', 'dropoffTime',
                           'enteringTime', 'exitingTime',
                           'pickUpTerminal',
                           'prevEndTerminal', 'prevTripEndTime',
                           'year', 'month', 'day', 'hour', 'dow',
                           'duration', 'fare',
                           'qrTime', 'productivity']
            new_headers += terminals
            writer.writerow(new_headers)
        #
        with open(ifpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                prevEndTerminal, pickUpTerminal = (row[hid[cn]] for cn in ['prevEndTerminal', 'pickUpTerminal'])
                pickupTime = eval(row[hid['pickupTime']])
                duration = eval(row[hid['duration']]) / 60.0  # Second -> Minute
                fare = eval(row[hid['fare']]) / 100.0  # Cent -> Dollar
                prevTripEndTime = eval(row[hid['prevTripEndTime']])
                if prevEndTerminal == pickUpTerminal:
                    qrTime = (pickupTime - eval(row[hid['prevTripEndTime']])) / 60.0  # Second -> Minute
                else:
                    if row[hid['enteringTime']] == 'inf':
                        qrTime = 0
                    else:
                        enteringTime = eval(row[hid['enteringTime']])
                        if enteringTime < pickupTime:
                            qrTime = (pickupTime - enteringTime) / 60.0  # Second -> Minute
                        else:
                            qrTime = 0
                productivity = fare / float(qrTime + duration) * 60  # Dollar/Minute -> Dollar/Hour
                new_row = [row[hid[cn]] for cn in ['did',
                                                   'pickupTime', 'dropoffTime',
                                                   'enteringTime', 'exitingTime',
                                                   'pickUpTerminal',
                                                   'prevEndTerminal', 'prevTripEndTime',
                                                   'year', 'month', 'day', 'hour', 'dow']]
                new_row += [duration, fare]
                new_row += [qrTime, productivity]
                for ter in terminals:
                    ter_df = df[(df['pickUpTerminal'] == ter)]
                    num_entered = len(ter_df[(ter_df['enteringTime'] <= prevTripEndTime)])
                    num_exited = len(ter_df[(ter_df['exitingTime'] <= prevTripEndTime)])
                    QN = num_entered - num_exited
                    new_row += [QN]
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
            new_row += [duration, fare]
            new_row += [year, month, day, hour, weekEnd]
            new_row += [qrTime, productivity]
            with open(filtered_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow(new_row)


if __name__ == '__main__':
    # filtering('09')
    filtering('10')

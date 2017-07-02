import __init__
from init_project import *
#
from _utils.logger import get_logger
#
from traceback import format_exc
from fnmatch import fnmatch
import pandas as pd
import csv

logger = get_logger()


def run(yymm):
    for fn in os.listdir(dpath['eeTime_ap']):
        if not fnmatch(fn, 'eeTime-ap-%s*.csv' % yymm):
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
            new_headers = ['vid', 'did',
                           'pickupTime', 'dropoffTime', 'duration', 'fare',
                           'enteringTime', 'exitingTime',
                           'pickUpTerminal',
                           'prevEndTerminal', 'prevTripEndTime',
                           'year', 'month', 'day', 'hour', 'dow',
                           'qrTime', 'productivity']
            new_headers += terminals
            writer.writerow(new_headers)
        #
        logger.info('handle the file; %s' % yymmdd)
        with open(ifpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                prevEndTerminal, pickUpTerminal = (row[hid[cn]] for cn in ['prevEndTerminal', 'pickUpTerminal'])
                pickupTime = eval(row[hid['pickupTime']])
                duration, fare = map(eval, (row[hid[cn]] for cn in ['duration', 'fare']))
                prevTripEndTime = eval(row[hid['prevTripEndTime']])
                if prevEndTerminal == pickUpTerminal:
                    qrTime = pickupTime - eval(row[hid['prevTripEndTime']])
                else:
                    if row[hid['enteringTime']] == 'inf':
                        qrTime = 0
                    else:
                        enteringTime = eval(row[hid['enteringTime']])
                        if enteringTime < pickupTime:
                            qrTime = pickupTime - enteringTime
                        else:
                            qrTime = 0
                new_row = [row[hid[cn]] for cn in ['vid', 'did',
                                                   'pickupTime', 'dropoffTime', 'duration', 'fare',
                                                   'enteringTime', 'exitingTime',
                                                   'pickUpTerminal',
                                                   'prevEndTerminal', 'prevTripEndTime',
                                                   'year', 'month', 'day', 'hour', 'dow']]
                new_row += [qrTime, fare / float(qrTime + duration)]
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


if __name__ == '__main__':
    run('0901')





from __path_organizer import *
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
    ofpath = opath.join(dpath['ap_QidQnum'], 'ap-QidQnum-%s.csv' % yymmdd)
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
            new_header += ['Qid']
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
                    Qid = -1
                else:
                    if locPrevDropoff == locPickup:  # Case 2
                        Qid = -2
                    else:
                        if row[hid['tEnter']] == 'inf':  # Case 3
                            Qid = -3
                        else:
                            tEnter = eval(row[hid['tEnter']])
                            if tPickUp < tEnter:  # Case 4
                                Qid = -4
                            else:
                                Qid = 0
                new_row = [row[hid[cn]] for cn in [
                                                    'year', 'month', 'day', 'dow', 'hour',
                                                    'did', 'fare',
                                                    'locPrevDropoff', 'locPickup', 'locDropoff',
                                                    'tPrevDropoff', 'tEnter', 'tExit',
                                                    'tripType',
                                                    'tFirstFree', 'tFirstOnCall', 'tPickUp', 'tDropOff']]
                new_row += [Qid]
                for ter in terminals:
                    ter_df = df[(df['locPickup'] == ter)]
                    num_entered = len(ter_df[(ter_df['tEnter'] <= tPrevDropoff)])
                    num_exited = len(ter_df[(ter_df['tExit'] <= tPrevDropoff)])
                    Qnum = num_entered - num_exited
                    new_row += [Qnum]
                with open(ofpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow(new_row)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymmdd), 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    pass
    # filtering('09')
    # filtering('10')

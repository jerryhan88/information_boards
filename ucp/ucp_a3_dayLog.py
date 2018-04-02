import sys, os
import os.path as opath
from datetime import datetime
import csv

AM2, AM5 = 2, 5


def run(log_dir):
    handling_day, vid_lastLoc = 0, {}
    for fn in sorted([fn for fn in os.listdir(log_dir) if fn.startswith('logs-')]):
        ifpath = opath.join(log_dir, fn)
        with open(ifpath) as r_csvfile:
            reader = csv.DictReader(r_csvfile)
            for row in reader:
                t = eval(row['time'])
                dt = datetime.fromtimestamp(t)
                if dt.day == 1 and dt.hour <= AM5:
                    continue
                if AM2 <= dt.hour and dt.hour <= AM5:
                    continue
                if dt.day != handling_day and dt.hour == AM5 + 1:
                    print('handling %dth day' % dt.day, datetime.now())
                    handling_day, vid_lastLoc = dt.day, {}
                    ofpath = opath.join(log_dir,
                                        'dayLog-%d%02d%02d.csv' % ((dt.year - 2000), dt.month, handling_day))
                    with open(ofpath, 'wt') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        new_headers = ['time', 'vid', 'apBasePos']
                        writer.writerow(new_headers)
                vid, apBasedPos = [row[cn] for cn in ['vid', 'apBasePos']]
                if vid in vid_lastLoc:
                    if vid_lastLoc[vid] != apBasedPos:
                        with open(ofpath, 'a') as w_csvfile:
                            writer = csv.writer(w_csvfile, lineterminator='\n')
                            writer.writerow([t, vid, apBasedPos])
                        vid_lastLoc[vid] = apBasedPos
                else:
                    with open(ofpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        writer.writerow([t, vid, apBasedPos])
                    vid_lastLoc[vid] = apBasedPos


if __name__ == '__main__':
    if len(sys.argv) == 2:
        log_dir = sys.argv[1]
    else:
        log_dir = os.getcwd()

    run(log_dir)

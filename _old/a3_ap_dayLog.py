import os.path as opath
import csv
from datetime import datetime
#
from __path_organizer import log_dpath, apDL_dpath

AM2, AM5 = 2, 5


def run(yymm):
    ifpath = opath.join(log_dpath, 'log-%s.csv' % yymm)
    #
    ofpath = None
    handling_day, vid_lastLoc = 0, {}
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
                handling_day, vid_lastLoc = dt.day, {}
                ofpath = opath.join(apDL_dpath, 'ap-dayLog-%s%02d.csv' % (yymm, handling_day))
                with open(ofpath, 'wt') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    new_header = ['time', 'taxi_id', 'driver_id', 'apBasePos']
                    writer.writerow(new_header)
            vid, did = map(int, [row[cn] for cn in ['taxi_id', 'driver_id']])
            apBasedPos = row['apBasePos']
            if did == -1:
                continue
            if vid in vid_lastLoc:
                if vid_lastLoc[vid] != apBasedPos:
                    with open(ofpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        writer.writerow([t, vid, did, apBasedPos])
                    vid_lastLoc[vid] = apBasedPos
            else:
                with open(ofpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow([t, vid, did, apBasedPos])
                vid_lastLoc[vid] = apBasedPos


if __name__ == '__main__':
    run('0901')
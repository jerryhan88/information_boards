import __init__
from init_project import *
#
from datetime import datetime
import csv


def run(yymm):
    ifpath = opath.join(dpath['log'], 'log-%s.csv' % yymm)
    ofpath = None
    handling_day, vid_lastLoc = 0, {}
    with open(ifpath, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        for row in reader:
            t = eval(row[hid['time']])
            dt = datetime.fromtimestamp(t)
            if dt.day == 1 and dt.hour <= AM5:
                continue
            if AM2 <= dt.hour and dt.hour <= AM5:
                continue
            if dt.day != handling_day and dt.hour == AM5 + 1:
                handling_day, vid_lastLoc = dt.day, {}
                ofpath = opath.join(dpath['ap_dayLog'], 'ap-dayLog-%s%02d.csv' % (yymm, handling_day))
                with open(ofpath, 'wt') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    new_headers = ['time', 'vid', 'did', 'state','apBasePos']
                    writer.writerow(new_headers)
            did = int(row[hid['did']])
            if did == -1:
                continue
            with open(ofpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow(row)
            # if vid_lastLoc.has_key(vid):
            #     if vid_lastLoc[vid] != apBasedPos:
            #         with open(ofpath, 'a') as w_csvfile:
            #             writer = csv.writer(w_csvfile, lineterminator='\n')
            #             writer.writerow([t, vid, did, apBasedPos])
            #         vid_lastLoc[vid] = apBasedPos
            # else:
            #     with open(ofpath, 'a') as w_csvfile:
            #         writer = csv.writer(w_csvfile, lineterminator='\n')
            #         writer.writerow([t, vid, did, apBasedPos])
            #     vid_lastLoc[vid] = apBasedPos


if __name__ == '__main__':
    run('0901')
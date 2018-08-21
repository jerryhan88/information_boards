import os.path as opath
import os
import sys
import multiprocessing
from datetime import datetime
import csv
#
from ucp_geoFunctions import get_ap_polygons
from __path_organizer import DATA_HOME

AVAILABLE, BUSY, HIRED, ON_CALL, CHANGE_SHIFT, OFFLINE = range(1, 7)
NUM_WORKERS = 11



def run(ifpath, dpath):

    fn = opath.basename(ifpath)
    print(fn)
    print(DATA_HOME)


    assert False

    ap_polygons = get_ap_polygons()
    with open(ifpath) as r_csvfile:
        reader = csv.DictReader(r_csvfile)
        for row in reader:
            vid, status = map(int, [row[cn] for cn in ['taxi_num_id', 'taxi_status']])
            lat, lon = map(float, [row[cn] for cn in ['latitude_val', 'longitude_val']])
            dt = datetime.strptime(row['min_time'], "%Y-%m-%d %H:%M:%S")



    assert False





    with open(ofpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        new_header = ['time', 'taxi_id', 'state', 'apBasePos']
        writer.writerow(new_header)
    #
    ap_polygons = get_ap_polygons()
    cur_day = -1
    with open(ifpath) as r_csvfile:
        reader = csv.DictReader(r_csvfile)
        for row in reader:
            vid, status = map(int, [row[cn] for cn in ['taxi_num_id', 'taxi_status']])
            lat, lon = map(float, [row[cn] for cn in ['latitude_val', 'longitude_val']])
            dt = datetime.strptime(row['min_time'], "%Y-%m-%d %H:%M:%S")
            if cur_day != dt.day:
                cur_day = dt.day
                print('Handling %d th day' % cur_day, datetime.now())
                if int(eDay) < cur_day:
                    print('Finish processes')
                    return
            if dt.day < int(sDay):
                continue
            new_row = [dt.timestamp(), vid, status]
            apBasePos = 'X'
            for ap_polygon in ap_polygons:
                if ap_polygon.is_including((lon, lat)):
                    apBasePos = ap_polygon.name
                    break
            new_row.append(apBasePos)

            with open(ofpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow(new_row)


if __name__ == '__main__':
    assert len(sys.argv) == 3
    ifpath, dpath = [sys.argv[i] for i in range(1, len(sys.argv))]
    if not opath.exists(dpath):
        os.mkdir(dpath)
    #
    run(ifpath, dpath)

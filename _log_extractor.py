import os.path as opath
import csv
from functools import reduce
from datetime import datetime
#
from util_geoFunctions import get_ap_polygons
from util_logging import logging
#
from __path_organizer import TAXI_RAW_DATA_HOME, test_dpath, lf_dpath



def run(yymmdd, hh=None, taxi_id=None):
    if type(taxi_id) != int:
        taxi_id = int(taxi_id)
    #
    logging_fpath = opath.join(test_dpath, '_test.txt')
    ofpath = opath.join(test_dpath, 'log-%s-%s-%s.csv' % (yymmdd, hh, taxi_id))
    logging(logging_fpath, 'handle the file; %s' % ofpath)
    with open(ofpath, 'w') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        new_header = ['time', 'taxi_id', 'driver_id', 'state', 'apBasePos']
        writer.writerow(new_header)
    #
    yymm = yymmdd[:len('yymm')]
    yy, mm = yymm[:len('yy')], yymm[len('yy'):]
    dd = yymmdd[len('yymm'):]
    yyyy = '20%s' % yy
    #
    log_fpath = reduce(opath.join, [TAXI_RAW_DATA_HOME,
                                    yyyy, mm, 'logs', 'logs-%s-normal.csv' % yymm])
    ap_polygons = get_ap_polygons()
    with open(log_fpath) as r_csvfile:
        reader = csv.DictReader(r_csvfile)
        for row in reader:
            t, vid, did, state = map(eval, [row[cn] for cn in ['time', 'vehicle-id', 'driver-id', 'state']])
            if vid != taxi_id:
                continue
            dt = datetime.fromtimestamp(t)
            if '%02d' % dt.day != dd:
                continue
            if '%02d' % dt.hour != hh:
                continue
            #
            lng, lat = map(eval, [row[cn] for cn in ['longitude', 'latitude']])
            new_row = [t, vid, did, state, lng, lat]
            apBasePos = 'X'
            for ap_polygon in ap_polygons:
                if ap_polygon.is_including((lng, lat)):
                    apBasePos = ap_polygon.name
                    break
            new_row.append(apBasePos)
            with open(ofpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow(new_row)


if __name__ == '__main__':
    run('091101', hh='05', taxi_id=8557)

import os.path as opath
import csv
from functools import reduce
#
from util_geoFunctions import get_ap_polygons
from util_logging import logging
#
from __path_organizer import TAXI_RAW_DATA_HOME, lf_dpath, log_dpath


def run(yymm):
    logging_fpath = opath.join(lf_dpath, 'a1_%s.txt' % yymm)
    ofpath = opath.join(log_dpath, 'log-%s.csv' % yymm)
    #
    logging(logging_fpath, 'handle the file; %s' % yymm)
    if opath.exists(ofpath):
        logging(logging_fpath, 'The file had already been processed; %s' % yymm)
        return None
    yy, mm = yymm[:2], yymm[2:]
    yyyy = '20%s' % yy
    #
    log_fpath = reduce(opath.join, [TAXI_RAW_DATA_HOME,
                                    yyyy, mm, 'logs', 'logs-%s-normal.csv' % yymm])
    ap_polygons = get_ap_polygons()
    #
    with open(log_fpath) as r_csvfile:
        reader = csv.DictReader(r_csvfile)
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_header = ['time', 'taxi_id', 'driver_id', 'state', 'apBasePos']
            writer.writerow(new_header)
            #
            for row in reader:
                new_row = [row[cn] for cn in ['time', 'vehicle-id', 'driver-id', 'state']]
                #
                lng, lat = map(eval, [row[cn] for cn in ['longitude', 'latitude']])
                apBasePos = 'X'
                for ap_polygon in ap_polygons:
                    if ap_polygon.is_including((lng, lat)):
                        apBasePos = ap_polygon.name
                        break
                new_row.append(apBasePos)
                #
                writer.writerow(new_row)
    logging(logging_fpath, 'end the file; %s' % yymm)


if __name__ == '__main__':
    run('0901')

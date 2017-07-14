import __init__
from init_project import *
#
from _utils.logger import get_logger
from _utils.geoFunctions import get_ap_polygons, get_ns_polygon
#
from os.path import expanduser
import csv
#
logger = get_logger()
TAXI_HOME = expanduser("~") + '/../taxi'


def run(yymm):
    ofpath = opath.join(dpath['log'], 'log-%s.csv' % yymm)
    if opath.exists(ofpath):
        logger.info('The file had already been processed; %s' % yymm)
        return None
    logger.info('handle the file; %s' % yymm)
    yy, mm = yymm[:2], yymm[2:]
    yyyy = '20%s' % yy
    log_fpath = opath(TAXI_HOME, '/%s/%s/logs/logs-%s-normal.csv' % (yyyy, mm, yymm))
    ap_polygons, ns_polygon = get_ap_polygons(), get_ns_polygon()
    #
    with open(log_fpath, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_headers = ['time', 'vid', 'did', 'state', 'apBasePos', 'nsBasePos']
            writer.writerow(new_headers)
            #
            for row in reader:
                new_row = [row[hid[cn]] for cn in ['time', 'vehicle-id', 'driver-id', 'state']]
                #
                lon, lat = map(eval, [row[hid[cn]] for cn in ['longitude', 'latitude']])
                apBasePos = 'X'
                for ap_polygon in ap_polygons:
                    if ap_polygon.is_including((lon, lat)):
                        apBasePos = ap_polygon.name
                        break
                new_row.append(apBasePos)
                new_row.append('O' if ns_polygon.is_including((lon, lat)) else 'X')
                #
                writer.writerow(new_row)
    logger.info('end the file; %s' % yymm)


if __name__ == '__main__':
    run('0901')

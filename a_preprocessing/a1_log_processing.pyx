import __init__
from init_project import *
#
from _utils.logger import get_logger
from _utils.geoFunctions import get_ap_polygons, get_ns_polygon
#
import csv
#
logger = get_logger()
#

def run(yymm):
    ofpath = opath.join(dpath['log'], 'log-%s.csv' % yymm)
    if opath.exists(ofpath):
        logger.info('The file had already been processed; %s' % yymm)
        return None
    logger.info('handle the file; %s' % yymm)
    log_fpath = opath.join(dpath['raw'], 'logs-%s-normal.csv' % yymm)
    ap_polygons, ns_polygon = get_ap_polygons(), get_ns_polygon()
    #
    with open(log_fpath, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_headers = ['time', 'vid', 'did', 'apBasePos', 'nsBasePos']
            writer.writerow(new_headers)
            #
            for row in reader:
                lon, lat = eval(row[hid['longitude']]), eval(row[hid['latitude']])
                apBasePos = 'X'
                for ap_polygon in ap_polygons:
                    res = ap_polygon.is_including((lon, lat))
                    if res:
                        apBasePos = ap_polygon.name
                        break
                nsBasePos = 'O' if ns_polygon.is_including((lon, lat)) else 'X'
                #
                new_row = [row[hid['time']], row[hid['vehicle-id']], row[hid['driver-id']],
                           apBasePos, nsBasePos]
                writer.writerow(new_row)
    logger.info('end the file; %s' % yymm)


if __name__ == '__main__':
    run('0901')

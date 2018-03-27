import sys
from datetime import datetime
import csv
#
from ucp_geoFunctions import get_ap_polygons


AVAILABLE, BUSY, HIRED, ON_CALL, CHANGE_SHIFT, OFFLINE = range(1, 7)


# [8, 13], [14, 20], [21, 27], [28, 30]

def run(ifpath, ofpath, sDay, eDay):
    with open(ofpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        new_header = ['time', 'vid', 'state', 'apBasePos']
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
                if int(eDay) < dt.day:
                    print('Finish processes')
                    return
                cur_day = dt.day
                print('Handling %d th day' % cur_day)
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
    if len(sys.argv) == 5:
        ifpath, ofpath, sDay, eDay = [sys.argv[i] for i in range(1, len(sys.argv))]
    else:
        ifpath = 'log_sample.csv'
        ofpath = 'log_out.csv'
        sDay, eDay = 1, 1

    run(ifpath, ofpath, sDay, eDay)

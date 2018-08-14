import sys
from datetime import datetime
import csv
#
from ucp_geoFunctions import get_ap_polygons
#


def run(ifpath, ofpath, sDay, eDay):
    with open(ofpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        new_header = [
                        'taxi_id', 'fare',
                        'start_time', 'end_time',
                        'tripType',
                        'start_loc', 'end_loc'
                     ]
        writer.writerow(new_header)
    #
    ap_polygons = get_ap_polygons()
    cur_vid = ''
    with open(ifpath) as r_csvfile:
        reader = csv.DictReader(r_csvfile)
        while True:
            try:
                row = next(reader)
                vid = row['taxi_num_id']
                start_dt = datetime.strptime(row['start_time'], "%Y-%m-%d %H:%M:%S")
                if cur_vid != vid:
                    cur_vid = vid
                    print('handling vid:', vid, datetime.now())
                if start_dt.day < int(sDay):
                    continue
                if int(eDay) < start_dt.day:
                    continue
                end_dt = datetime.strptime(row['end_time'], "%Y-%m-%d %H:%M:%S")
                trip_type = row['trip_type']
                new_row = [vid, row['fare'], start_dt.timestamp(), end_dt.timestamp(), trip_type]

                start_lat, start_lon = map(float,
                                           [row[cn] for cn in ['start_latitude', 'start_longitude']])
                apBasePos = 'X'
                for ap_polygon in ap_polygons:
                    if ap_polygon.is_including((start_lon, start_lat)):
                        apBasePos = ap_polygon.name
                        break
                new_row.append(apBasePos)

                end_lat, end_lon = map(float,
                                       [row[cn] for cn in ['end_latitude', 'end_longitude']])
                apBasePos = 'X'
                for ap_polygon in ap_polygons:
                    if ap_polygon.is_including((end_lon, end_lat)):
                        apBasePos = ap_polygon.name
                        break
                new_row.append(apBasePos)
                with open(ofpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow(new_row)
            except csv.Error:
                continue
            except StopIteration:
                break


if __name__ == '__main__':
    if len(sys.argv) == 5:
        ifpath, ofpath, sDay, eDay = [sys.argv[i] for i in range(1, len(sys.argv))]
    else:
        ifpath = 'trip_sample.csv'
        ofpath = 'trip_out.csv'
        sDay, eDay = 1, 1

    run(ifpath, ofpath, sDay, eDay)

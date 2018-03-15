import os.path as opath
from datetime import datetime
import csv


log_fn = 'log_sample.csv'
trip_fn = 'trip_sample.csv'

AVAILABLE, BUSY, HIRED, ON_CALL, CHANGE_SHIFT, OFFLINE = range(1, 7)


vehicles = {}

with open(log_fn) as r_csvfile:
    reader = csv.DictReader(r_csvfile)
    for row in reader:
        vid, status = map(int, [row[cn] for cn in ['taxi_num_id', 'taxi_status']])
        lat, lon = map(float, [row[cn] for cn in ['latitude_val', 'longitude_val']])
        dt = datetime.strptime(row['min_time'], "%Y-%m-%d %H:%M:%S")
        if vid not in vehicles:
            pass
        print(dt)

        assert False

        # print(vid, lambda )






# with open(fpath, 'wt') as w_csvfile:
#     writer = csv.writer(w_csvfile, lineterminator='\n')
#     new_header = ['Scheduled', 'Updated', 'From', 'Flight', 'Terminal', 'Belt', 'Status']
#     writer.writerow(new_header)



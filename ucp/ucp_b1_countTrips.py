import sys, os
import os.path as opath
import pandas as pd
import csv
import xlwt


def run(trip_dir, ofpath1, ofpath2):
    if not opath.exists(ofpath1):
        df = None
        for fn in sorted([fn for fn in os.listdir(trip_dir) if fn.startswith('dayTrip') and fn.endswith('.csv')]):
            trip_fpath = opath.join(trip_dir, fn)
            if df is None:
                df = pd.read_csv(trip_fpath)
            else:
                df = df.append(pd.read_csv(trip_fpath))
            print(len(df), fn)

        df = df.groupby(['year', 'month', 'day', 'hour', 'locPrevDropoff', 'locPickup']).count()['tripType'].reset_index()
        df = df.rename(columns={'locPrevDropoff': 'origin', 'locPickup': 'destination', 'tripType': 'flow'})
        df['origin'][df['origin'] == 'BudgetT'] = 'BT'
        df['origin'][df['origin'] == 'X'] = 'XAP'
        df['destination'][df['destination'] == 'BudgetT'] = 'BT'
        df['destination'][df['destination'] == 'X'] = 'XAP'
        df.to_csv(ofpath1, index=False)
    else:
        df = pd.read_csv(ofpath1)
    df = df.groupby(['origin', 'destination']).sum()['flow'].reset_index()
    df.to_csv(ofpath2, index=False)


def gen_xlsx_files():
    ifpath = 'tripCountHour-1704.csv'


    flow = {}
    with open(ifpath) as r_csvfile:
        reader = csv.DictReader(r_csvfile)
        for row in reader:
            hour = int(row['hour'])
            ori, dest = [row[cn] for cn in ['origin', 'destination']]
            flow[hour, ori, dest] = int(row['flow'])

    hours = [0, 1] + list(range(6, 24))
    sorting_order = ['T1', 'T2', 'T3', 'BT', 'XAP']

    for h in hours:
        ofpath = 'AirportFlow_H%02d_Apri_2017.xls' % h
        wb = xlwt.Workbook()
        ws = wb.add_sheet('RawNumber')
        for i, ori in enumerate(sorting_order):
            for j, dest in enumerate(sorting_order):
                ws.write(i + 2, j + 1, flow[h, ori, dest] if (h, ori, dest) in flow else 0)
        wb.save(ofpath)


if __name__ == '__main__':
    gen_xlsx_files()



    # if len(sys.argv) == 4:
    #     trip_fpath, ofpath1, ofpath2 = [sys.argv[i] for i in range(1, 4)]
    # else:
    #     assert False
    #
    # run(trip_fpath, ofpath1, ofpath2)
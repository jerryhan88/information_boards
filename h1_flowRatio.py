import os.path as opath
import os
import pandas as pd
import csv
import xlwt



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
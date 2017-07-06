import __init__
from init_project import *
#
import pandas as pd
import csv


def run(yy):
    ifpath = opath.join(dpath['qrTimeTerNumber_ap'], 'Filtered-qrTimeTerNumber-ap-20%s.csv' % yy)
    df = pd.read_csv(ifpath)
    df = df[(df['prevEndTerminal'] != 'X')]
    df.year = df.year.astype(int)
    df.month = df.month.astype(int)
    df.day = df.day.astype(int)
    df.hour = df.hour.astype(int)
    pickupO_df, pickupX_df = df[(df['pickUpTerminal'] != 'X')], df[(df['pickUpTerminal'] == 'X')]
    loc_hour_prod = {}
    for pickupLoc, pickup_df in [('O', pickupO_df), ('X', pickupX_df)]:
        loc_hour_prod[pickupLoc] = {}
        group_df = pickup_df.groupby(['year', 'month', 'day', 'hour']).sum().reset_index()
        for year, month, day, hour, duration ,qrTime, fare in \
                    group_df[['year', 'month', 'day', 'hour', 'duration', 'qrTime', 'fare']].values:
            loc_hour_prod[pickupLoc][year, month, day, hour] = fare / float(duration + qrTime)
    #
    ofpath = opath.join(dpath['analysis'], 'decision-ap-20%s.csv' % yy)
    hid = {cn: i for i, cn in enumerate(df.columns)}
    with open(ofpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        new_header = list(df.columns)
        new_header += ['oppoCost', 'ecoProfit']
        new_header += ['sumQnum', 'pickupTQnum', 'minTerminal', 'minTQnum']
        writer.writerow(new_header)
    #
    df.sort_values(['year', 'month', 'day', 'hour'], ascending=[True] * 4)
    terminals = set(df['pickUpTerminal'])
    for row in df.values:
        year, month, day, hour = map(int, [row[hid[cn]] for cn in ['year', 'month', 'day', 'hour']])
        pickUpTerminal = row[hid['pickUpTerminal']]
        duration, qrTime, fare = [row[hid[cn]] for cn in ['duration', 'qrTime', 'fare']]
        try:
            if pickUpTerminal == 'X':
                oppoCost = (duration + qrTime) * loc_hour_prod['O'][year, month, day, hour]
            else:
                oppoCost = (duration + qrTime) * loc_hour_prod['X'][year, month, day, hour]
        except KeyError:
            continue
        ecoProfit = fare - oppoCost
        minTerminal, minTQnum = None, 1e400
        pickupTQnum = -1
        sumQnum = 0
        for tn in terminals:
            Qnum = row[hid[tn]]
            if tn == pickUpTerminal:
                assert pickupTQnum == -1
                pickupTQnum = Qnum
            if Qnum < minTQnum:
                minTQnum = Qnum
                minTerminal = tn
            sumQnum += Qnum
        with open(ofpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_row = [row[hid[cn]] for cn in df.columns]
            new_row += [oppoCost, ecoProfit]
            new_row += [sumQnum, pickupTQnum, minTerminal, minTQnum]
            writer.writerow(new_row)


if __name__ == '__main__':
    run('10')
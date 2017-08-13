import __init__
from init_project import *
#
import pandas as pd
import csv


def basicProcess(yy):
    ifpath = opath.join(dpath['ap_QidQnum'], 'ap-QidQnum-20%s.csv' % yy)
    df = pd.read_csv(ifpath)
    df = df.sort_values(['tPickUp'], ascending=[True])
    #
    df['tMaxFirstFreePrevDropoff'] = df.apply(lambda row: row['tFirstFree'] if row['tPrevDropoff'] < row['tFirstFree'] else row['tPrevDropoff'], axis=1)
    df['cycleTime'] = df['tDropOff'] - df['tMaxFirstFreePrevDropoff']
    df['productivity'] = df['fare'] / df['cycleTime']
    #
    df['fare'] = df['fare'] / CENT
    df['cycleTime'] = df['cycleTime'] / MIN1
    df['productivity'] = df['productivity'] * HOUR1 / CENT
    #
    df = df[(df['tPrevDropoff'] < df['tPickUp'])]
    df = df[(df['tFirstFree'] < df['tPickUp'])]
    df = df[(df['cycleTime'] < (HOUR2 / MIN1))]
    df = df[(df['productivity'] < TH_PRODUCTIVITY)]
    #
    ofpath = opath.join(dpath['analysis'], 'ap-whole-20%s.csv' % yy)
    df.to_csv(ofpath, index=False)
    #
    groupby_df = df.groupby(['year', 'month', 'day', 'hour']).sum().reset_index()
    new_df = groupby_df[['year', 'month', 'day', 'hour', 'fare', 'cycleTime']]
    new_df['productivity'] = new_df['fare'] / new_df['cycleTime'] * MIN1
    ofpath = opath.join(dpath['analysis'], 'ap-whole-hourProductivity-20%s.csv' % yy)
    new_df.to_csv(ofpath, index=False)


def dropoffAP_dataProcess(yy):
    ifpath = opath.join(dpath['analysis'], 'ap-whole-20%s.csv' % yy)
    df = pd.read_csv(ifpath)
    GA_df, GO_df = df[(df['locPickup'] != 'X')], df[(df['locPickup'] == 'X')]
    GA_fpath = opath.join(dpath['analysis'], 'dropoffAP-GA-hourProductivity-20%s.csv' % yy)
    GO_fpath = opath.join(dpath['analysis'], 'dropoffAP-GO-hourProductivity-20%s.csv' % yy)
    for df, ofpath in [(GA_df, GA_fpath),
                       (GO_df, GO_fpath)]:
        groupby_df = df.groupby(['year', 'month', 'day', 'hour']).sum().reset_index()
        new_df = groupby_df[['year', 'month', 'day', 'hour', 'fare', 'cycleTime']]
        new_df['productivity'] = new_df['fare'] / new_df['cycleTime'] * MIN1
        new_df.to_csv(ofpath, index=False)
    GA_hourProductivity, GO_hourProductivity = {}, {}
    for fare_cycleTime, ifpath in [(GA_hourProductivity, GA_fpath),
                                   (GO_hourProductivity, GO_fpath)]:
        with open(ifpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            header = reader.next()
            hid = {h: i for i, h in enumerate(header)}
            for row in reader:
                year, month, day, hour = map(int, [row[hid[cn]] for cn in ['year', 'month', 'day', 'hour']])
                fare_cycleTime[year, month, day, hour] = eval(row[hid['productivity']])
    #
    ifpath = opath.join(dpath['analysis'], 'ap-whole-20%s.csv' % yy)
    ofpath = opath.join(dpath['analysis'], 'dropoffAP-20%s.csv' % yy)
    with open(ifpath, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        header = reader.next()
        hid = {h: i for i, h in enumerate(header)}
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_header = header[:] + ['QTime', 'durTillPickup', 'oppoCost', 'ecoProfit', 'J']
            writer.writerow(new_header)
            for row in reader:
                locPrevDropoff, locPickup = [row[hid[cn]] for cn in ['locPrevDropoff', 'locPickup']]
                if locPrevDropoff == 'X':
                    continue
                year, month, day, hour = map(int, [row[hid[cn]] for cn in ['year', 'month', 'day', 'hour']])
                Qid = int(row[hid['Qid']])
                fare, cycleTime, tPickUp = map(eval, [row[hid[cn]] for cn in ['fare', 'cycleTime', 'tPickUp']])
                durTillPickup = (tPickUp  - eval(row[hid['tMaxFirstFreePrevDropoff']])) / MIN1
                if locPickup == 'X':
                    J = 0
                    assert Qid == -1
                    QTime = -1
                    try:
                        oppoCost = (cycleTime / MIN1) * GA_hourProductivity[year, month, day, hour]
                    except KeyError:
                        continue
                else:
                    J = 1
                    if locPrevDropoff == locPickup:
                        assert Qid == -2
                        QTime = (tPickUp - eval(row[hid['tPrevDropoff']])) / MIN1
                    else:
                        if row[hid['tEnter']] == 'inf':
                            assert Qid == -3
                            continue
                        else:
                            tEnter = eval(row[hid['tEnter']])
                            if tPickUp < tEnter:  # Case 4
                                assert Qid == -4
                                continue
                            else:
                                QTime = (tPickUp - tEnter) / MIN1
                    if cycleTime < QTime:
                        continue
                    oppoCost = (cycleTime / MIN1) * GO_hourProductivity[year, month, day, hour]
                ecoProfit = fare - oppoCost
                #
                new_row = row[:] + [QTime, durTillPickup, oppoCost, ecoProfit, J]
                writer.writerow(new_row)


def pickupAP_dataProcess(yy):
    ifpath = opath.join(dpath['analysis'], 'ap-whole-20%s.csv' % yy)
    ofpath = opath.join(dpath['analysis'], 'pickupAP-20%s.csv' % yy)
    with open(ifpath, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        header = reader.next()
        hid = {h: i for i, h in enumerate(header)}
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_header = header[:] + ['QTime', 'durTillPickup', 'X']
            writer.writerow(new_header)
            for row in reader:
                locPrevDropoff, locPickup = [row[hid[cn]] for cn in ['locPrevDropoff', 'locPickup']]
                if locPickup == 'X':
                    continue
                Qid = int(row[hid['Qid']])
                assert Qid != -1
                tPickUp = eval(row[hid['tPickUp']])
                if locPrevDropoff == locPickup:
                    assert Qid == -2
                    QTime = (tPickUp - eval(row[hid['tPrevDropoff']])) / MIN1
                else:
                    if row[hid['tEnter']] == 'inf':
                        assert Qid == -3
                        continue
                    else:
                        tEnter = eval(row[hid['tEnter']])
                        if tPickUp < tEnter:  # Case 4
                            assert Qid == -4
                            continue
                        else:
                            QTime = (tPickUp - tEnter) / MIN1
                if eval(row[hid['cycleTime']]) < QTime:
                    continue
                durTillPickup = (eval(row[hid['tPickUp']]) - eval(row[hid['tMaxFirstFreePrevDropoff']])) / MIN1
                X = 0 if row[hid['locPrevDropoff']] == 'X' else 1
                #
                new_row = row[:] + [QTime, durTillPickup, X]
                writer.writerow(new_row)


def dropoffAP_pickupAP_dataProcess(yy):
    ifpath = opath.join(dpath['analysis'], 'ap-whole-20%s.csv' % yy)
    ofpath = opath.join(dpath['analysis'], 'dropoffAP-pickupAP-20%s.csv' % yy)
    with open(ifpath, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        header = reader.next()
        hid = {h: i for i, h in enumerate(header)}
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_header = header[:] + ['QTime', 'durTillPickup']
            writer.writerow(new_header)
            for row in reader:
                locPrevDropoff, locPickup = [row[hid[cn]] for cn in ['locPrevDropoff', 'locPickup']]
                if locPrevDropoff == 'X':
                    continue
                if locPickup == 'X':
                    continue
                Qid = int(row[hid['Qid']])
                assert Qid != -1
                tPickUp = eval(row[hid['tPickUp']])
                if locPrevDropoff == locPickup:
                    assert Qid == -2
                    QTime = (tPickUp - eval(row[hid['tPrevDropoff']])) / MIN1
                else:
                    if row[hid['tEnter']] == 'inf':
                        assert Qid == -3
                        continue
                    else:
                        tEnter = eval(row[hid['tEnter']])
                        if tPickUp < tEnter:  # Case 4
                            assert Qid == -4
                            continue
                        else:
                            QTime = (tPickUp - tEnter) / MIN1
                if eval(row[hid['cycleTime']]) < QTime:
                    continue
                durTillPickup = (tPickUp  - eval(row[hid['tMaxFirstFreePrevDropoff']])) / MIN1
                #
                new_row = row[:] + [QTime, durTillPickup]
                writer.writerow(new_row)


def dropoffAP_pickupX_dataProcess(yy):
    ifpath = opath.join(dpath['analysis'], 'ap-whole-20%s.csv' % yy)
    ofpath = opath.join(dpath['analysis'], 'dropoffAP-pickupX-20%s.csv' % yy)
    with open(ifpath, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        header = reader.next()
        hid = {h: i for i, h in enumerate(header)}
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_header = header[:] + ['durTillPickup']
            writer.writerow(new_header)
            for row in reader:
                locPrevDropoff, locPickup = [row[hid[cn]] for cn in ['locPrevDropoff', 'locPickup']]
                if locPrevDropoff == 'X':
                    continue
                if locPickup != 'X':
                    continue
                tPickUp = eval(row[hid['tPickUp']])
                durTillPickup = (tPickUp  - eval(row[hid['tMaxFirstFreePrevDropoff']])) / MIN1
                #
                new_row = row[:] + [durTillPickup]
                writer.writerow(new_row)


if __name__ == '__main__':
    # basicProcess('09')
    # basicProcess('10')
    #
    # dropoffAP_dataProcess('09')
    # dropoffAP_dataProcess('10')
    #
    # pickupAP_dataProcess('09')
    # pickupAP_dataProcess('10')

    # dropoffAP_pickupAP_dataProcess('09')
    # dropoffAP_pickupAP_dataProcess('10')

    # dropoffAP_pickupX_dataProcess('09')
    dropoffAP_pickupX_dataProcess('10')
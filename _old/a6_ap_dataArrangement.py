import os.path as opath
import os
import pandas as pd
import csv
#
from __path_organizer import apDT_dpath


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
    holidays = HOLIDAYS2009 if yy == '09' else HOLIDAYS2010
    df['workingDay'] = df.apply(lambda row: 0 if (row['dow'] in WEEKENDS) or
                                                 ((row['year'], row['month'], row['day']) in holidays) else 1,
                                axis=1)
    #
    ofpath = opath.join(dpath['_data'], 'wholeAP-20%s.csv' % yy)
    df.to_csv(ofpath, index=False)
    #
    groupby_df = df.groupby(['year', 'month', 'day', 'hour']).sum().reset_index()
    new_df = groupby_df[['year', 'month', 'day', 'hour', 'fare', 'cycleTime']]
    new_df['productivity'] = new_df['fare'] / new_df['cycleTime'] * MIN1
    ofpath = opath.join(dpath['_data'], 'wholeAP-hourProductivity-20%s.csv' % yy)
    new_df.to_csv(ofpath, index=False)


def wholeAP_QNum(yy):
    ifpath = opath.join(dpath['_data'], 'wholeAP-20%s.csv' % yy)
    ofpath = opath.join(dpath['_data'], 'wholeAP-QNum-20%s.csv' % yy)
    terminals = ['T1', 'T2', 'T3', 'BudgetT']
    labels = ['year', 'month', 'day', 'dow', 'hour', 'terminal', 'QNum']
    records = []
    processed_date_hour = set()
    with open(ifpath, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        header = reader.next()
        hid = {h: i for i, h in enumerate(header)}
        for row in reader:
            year, month, day, dow, hour = map(int, [row[hid[cn]] for cn in ['year', 'month', 'day', 'dow', 'hour']])
            k = (year, month, day, hour)
            if k in processed_date_hour:
                continue
            processed_date_hour.add(k)
            for tn in terminals:
                QNum = int(row[hid[tn]])
                records.append([year, month, day, dow, hour, tn, QNum])
    df = pd.DataFrame.from_records(records, columns=labels)
    df.to_csv(ofpath, index=False)


def dropoff_dataProcess(yy, isAP=True):
    prefix = 'dropoffAP' if isAP else 'dropoffXAP'
    GA_fpath = opath.join(dpath['_data'], '%s-GA-hourProductivity-20%s.csv' % (prefix, yy))
    GO_fpath = opath.join(dpath['_data'], '%s-GO-hourProductivity-20%s.csv' % (prefix, yy))
    #
    ifpath = opath.join(dpath['_data'], 'wholeAP-20%s.csv' % yy)
    df = pd.read_csv(ifpath)
    if isAP:
        df = df[(df['locPrevDropoff'] != 'X')]
    else:
        df = df[(df['locPrevDropoff'] == 'X')]
    GA_df, GO_df = df[(df['locPickup'] != 'X')], df[(df['locPickup'] == 'X')]
    for df, ofpath, GA in [(GA_df, GA_fpath, 1),
                           (GO_df, GO_fpath, 0)]:
        groupby_df = df.groupby(['year', 'month', 'day', 'hour']).sum().reset_index()
        new_df = groupby_df[['year', 'month', 'day', 'hour', 'fare', 'cycleTime']]
        new_df['productivity'] = new_df['fare'] / new_df['cycleTime'] * MIN1
        new_df['GA'] = GA
        new_df.to_csv(ofpath, index=False)
    #
    for df, ofpath, GA in [(GA_df, GA_fpath, 1),
                           (GO_df, GO_fpath, 0)]:
        groupby_df = df.groupby(['year', 'month', 'day', 'hour']).sum().reset_index()
        new_df = groupby_df[['year', 'month', 'day', 'hour', 'fare', 'cycleTime']]
        new_df['productivity'] = new_df['fare'] / new_df['cycleTime'] * MIN1
        new_df['GA'] = GA
        new_df.to_csv(ofpath, index=False)
    #
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
    ifpath = opath.join(dpath['_data'], 'wholeAP-20%s.csv' % yy)
    ofpath = opath.join(dpath['_data'], '%s-20%s.csv' % (prefix, yy))
    with open(ifpath, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        header = reader.next()
        hid = {h: i for i, h in enumerate(header)}
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_header = header[:] + ['QTime', 'sunkCost', 'oppoCost', 'ecoProfit',
                                      'GA', 'DScore', 'productivityGA', 'productivityGO']
            writer.writerow(new_header)
            for row in reader:
                locPrevDropoff, locPickup = [row[hid[cn]] for cn in ['locPrevDropoff', 'locPickup']]
                if isAP:
                    if locPrevDropoff == 'X':
                        continue
                else:
                    if locPrevDropoff != 'X':
                        continue
                year, month, day, hour = map(int, [row[hid[cn]] for cn in ['year', 'month', 'day', 'hour']])
                Qid = int(row[hid['Qid']])
                fare, cycleTime, tPickUp = map(eval, [row[hid[cn]] for cn in ['fare', 'cycleTime', 'tPickUp']])
                sunkCost = (tPickUp - eval(row[hid['tMaxFirstFreePrevDropoff']])) / MIN1
                try:
                    productivity_GA = GA_hourProductivity[year, month, day, hour]
                    productivity_GO = GO_hourProductivity[year, month, day, hour]
                except KeyError:
                    continue
                if locPickup == 'X':
                    GA = 0
                    assert Qid == -1
                    QTime = -1
                    oppoCost = (cycleTime / MIN1) * productivity_GA
                else:
                    GA = 1
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
                    oppoCost = (cycleTime / MIN1) * productivity_GO
                ecoProfit = fare - oppoCost
                diff = abs(productivity_GA - productivity_GO)
                if productivity_GA > productivity_GO:
                    if GA == 1:
                        DScore = diff
                    else:
                        DScore = -1 * diff
                else:
                    if GA == 1:
                        DScore = -1 * diff
                    else:
                        DScore = diff
                #
                new_row = row + [QTime, sunkCost, oppoCost, ecoProfit,
                                 GA, DScore, productivity_GA, productivity_GO]
                writer.writerow(new_row)


def pickupAP_dataProcess(yy):
    ifpath = opath.join(dpath['_data'], 'wholeAP-20%s.csv' % yy)
    pickupAP_ofpath = opath.join(dpath['_data'], 'pickupAP-20%s.csv' % yy)
    with open(ifpath, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        header = reader.next()
        hid = {h: i for i, h in enumerate(header)}
        with open(pickupAP_ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_header = header + ['QTime', 'sunkCost', 'FA']
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
                sunkCost = (eval(row[hid['tPickUp']]) - eval(row[hid['tMaxFirstFreePrevDropoff']])) / MIN1
                FA = 0 if row[hid['locPrevDropoff']] == 'X' else 1
                #
                new_row = row[:] + [QTime, sunkCost, FA]
                writer.writerow(new_row)
    df = pd.read_csv(pickupAP_ofpath)
    gdf = df.groupby(['year', 'month', 'day', 'hour', 'locPickup']).mean()['QTime'].to_frame('avgQTime').reset_index()
    dateTerminal_avgQTime = {}
    dates, terminals = set(), set()
    for year, month, day, hour, locPickup, avgQTime in gdf.values:
        date = (year, month, day, hour)
        dates.add(date)
        terminals.add(locPickup)
        dateTerminal_avgQTime[date, locPickup] = avgQTime
    pickupAP_DScore_ofpath = opath.join(dpath['_data'], 'pickupAP-DScore-20%s.csv' % yy)
    dates, terminals = map(sorted, map(list, [dates, terminals]))
    with open(pickupAP_DScore_ofpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        new_header = ['year', 'month', 'day', 'hour'] + terminals
        writer.writerow(new_header)
    terminalDScore = {}
    for date in dates:
        year, month, day, hour = date
        terminalAvgQtime = []
        for tn in terminals:
            try:
                terminalAvgQtime.append((dateTerminal_avgQTime[date, tn], tn))
            except KeyError:
                terminalAvgQtime.append((1e400, tn))
        terminalAvgQtime.sort(reverse=True)
        for i, (_, tn) in enumerate(terminalAvgQtime):
            terminalDScore[year, month, day, hour, tn] = i
        with open(pickupAP_DScore_ofpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_row = [year, month, day, hour]
            new_row += [terminalDScore[year, month, day, hour, tn] for tn in terminals]
            writer.writerow(new_row)
    #
    df['DScore'] = df.apply(lambda row: terminalDScore[row['year'], row['month'], row['day'], row['hour'], row['locPickup']],
                            axis=1)
    df.to_csv(pickupAP_ofpath, index=False)


if __name__ == '__main__':
    pass





    # basicProcess('09')
    # basicProcess('10')
    #
    # wholeAP_QNum('09')
    # wholeAP_QNum('10')
    #
    # dropoff_dataProcess('09')
    # dropoff_dataProcess('10')
    # dropoff_dataProcess('09', isAP=False)
    # dropoff_dataProcess('10', isAP=False)
    #
    # pickupAP_dataProcess('09')
    # pickupAP_dataProcess('10')

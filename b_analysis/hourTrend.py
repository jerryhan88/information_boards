import __init__
from init_project import *
#
import pandas as pd
import seaborn as sns; sns.set_style("whitegrid")
import matplotlib.pyplot as plt
import numpy as np
import csv


_figsize = (8, 6)


def run_numTrips():
    def process_numTrips(_df, img_ofpath):
        dows, hours = set(), set()
        dowHour_numTrips = {}
        for dow, hour, numTrips in _df.groupby(['dow', 'hour']).count()['did'].to_frame('numTrips').reset_index().values:
            dows.add(dow)
            hours.add(hour)
            k = (dow, hour)
            if not dowHour_numTrips.has_key(k):
                dowHour_numTrips[k] = 0
            dowHour_numTrips[k] += numTrips
        dows, hours = map(sorted, map(list, [dows, hours]))
        fig = plt.figure(figsize=_figsize)
        ax = fig.add_subplot(111)
        ax.set_xlabel('hour')
        ax.set_ylabel('numTrips')
        for dow in dows:
            plt.plot(range(len(hours)), [dowHour_numTrips[dow, hour] for hour in hours])
        plt.legend(['Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat', 'Sun'], ncol=1, loc='upper left')
        plt.xticks(range(len(hours)), hours)
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    df = pd.read_csv(opath.join(dpath['_data'], 'wholeAP-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'wholeAP-2010.csv')))
    #
    img_ofpath = opath.join(dpath['numTrips'], 'hourTrendNumTrips.pdf')
    process_numTrips(df, img_ofpath)
    #
    img_ofpath = opath.join(dpath['numTrips'], 'hourTrendNumTripsDropoff.pdf')
    process_numTrips(df[(df['locPrevDropoff'] != 'X')], img_ofpath)
    for year in [2009, 2010]:
        img_ofpath = opath.join(dpath['numTrips'], 'hourTrendNumTripsDropoff%d.pdf' % year)
        process_numTrips(df[(df['locPrevDropoff'] != 'X') & (df['year'] == year)], img_ofpath)

    #
    img_ofpath = opath.join(dpath['numTrips'], 'hourTrendNumTripsPickup.pdf')
    process_numTrips(df[(df['locPickup'] != 'X')], img_ofpath)
    #
    for year in [2009, 2010]:
        img_ofpath = opath.join(dpath['numTrips'], 'hourTrendNumTripsPickup%d.pdf' % year)
        process_numTrips(df[(df['locPickup'] != 'X') & (df['year'] == year)], img_ofpath)


def run_QTimeTerminal():
    m = 'QTime'
    #
    df = pd.read_csv(opath.join(dpath['_data'], 'pickupAP-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'pickupAP-2010.csv')))
    img_ofpath = opath.join(dpath['hourTrendPickupAP'], 'hourTrendPickupAP-%s.pdf' % m)
    groupby_df = df.groupby(['year', 'month', 'day', 'hour', 'locPickup']).mean().reset_index()
    
    yy = '09'
    img_ofpath = opath.join(dpath['hourTrend'], 'hourTrendQTimeTerminal-20%s.pdf' % yy)
    dfYear = groupby_df[(groupby_df['year'] == 2009)]
    _figsize = (8, 6)
    fig = plt.figure(figsize=_figsize)
    fig.add_subplot(111)
    sns.barplot(x="hour", y="QTime", hue="locPickup", hue_order = ['T1', 'T2', 'T3', 'BudgetT'], data=dfYear)
    plt.ylim((0, 100))
    plt.yticks(np.arange(0, 100, 20))
    plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    #
    df.groupby(['year', 'hour']).std().reset_index()[['year', 'hour', 'QTime']]
    
    
    
    
    for year, month, day, hour, locPickup, QTime in groupby_df[['year', 'month', 'day', 'hour', 'locPickup', 'QTime']].values:
        
        print year
        assert False
        records.append([yyyy, hour, i, count, count / float(hour_wholeCount[hour])])
    


def run_QNum():
    for yy in ['09', '10']:
        ifpath = opath.join(dpath['_data'], 'wholeAP-20%s.csv' % yy)
        csv_ofpath = opath.join(dpath['hourTrendQNum'], 'hourTrendQNum-20%s.csv' % yy)
        #
        terminals = ['T1', 'T2', 'T3', 'BudgetT']
        labels = ['year', 'month', 'day', 'dow', 'hour', 'QNum', 'terminal']
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
                    records.append([year, month, day, dow, hour, QNum, tn])
        df = pd.DataFrame.from_records(records, columns=labels)
        df.to_csv(csv_ofpath, index=False)
        #
        img_ofpath = opath.join(dpath['hourTrendQNum'], 'hourTrendQNum-20%s.pdf' % yy)
        _figsize = (8, 6)
        fig = plt.figure(figsize=_figsize)
        fig.add_subplot(111)
        sns.barplot(x="hour", y="QNum", hue="terminal", data=df)
        plt.ylim((0, 100))
        plt.yticks(np.arange(0, 100, 20))
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
        #
        for dow in set(df['dow']):
            dow_df = df[(df['dow'] == dow)]
            img_ofpath = opath.join(dpath['hourTrendQNum'], 'hourTrendQNum-20%s-%s.pdf' % (yy, dow))
            _figsize = (8, 6)
            fig = plt.figure(figsize=_figsize)
            fig.add_subplot(111)
            sns.barplot(x="hour", y="QNum", hue="terminal", data=dow_df)
            plt.ylim((0, 100))
            plt.yticks(np.arange(0, 100, 20))
            plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)



def run_pickupAPBefore():
    csv_ofpath = opath.join(dpath['hourTrendPickupAP'], 'hourTrendPickupAP-count-percent.csv')
    labels = ['year', 'hour', 'beforeAP', 'count', 'percent']
    records = []
    for yy in ['09', '10']:
        yyyy = int('20%s' % yy)
        df = pd.read_csv(opath.join(dpath['_data'], 'pickupAP-20%s.csv' % yy))
        hour_wholeCount = {hour: count for hour, count in df.groupby(['hour']).count().reset_index()[['hour', 'did']].values}
        dfX, dfO = df[(df['locPrevDropoff'] == 'X')], df[(df['locPrevDropoff'] != 'X')]
        for i, df_ in enumerate([dfX, dfO]):
            groupby_df = df_.groupby(['hour']).count().reset_index()
            for hour, count in groupby_df[['hour', 'did']].values:
                records.append([yyyy, hour, i, count, count / float(hour_wholeCount[hour])])
    df = pd.DataFrame.from_records(records, columns=labels)
    df.to_csv(csv_ofpath, index=False)

    for m in ['count', 'percent']:
        img_ofpath = opath.join(dpath['hourTrendPickupAP'], 'hourTrendPickupAP-%s.pdf' % m)
        _figsize = (8, 6)
        fig = plt.figure(figsize=_figsize)
        fig.add_subplot(111)
        sns.barplot(x="hour", y=m, hue="year", data=df)
        if m == 'percent':
            plt.ylim((0.0, 1.0))
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)

    for i, beforeAP in enumerate(['beforeAPX', 'beforeAPO']):
        dow_df = df[(df['beforeAP'] == i)]
        for m in ['count', 'percent']:
            img_ofpath = opath.join(dpath['hourTrendPickupAP'], 'hourTrendPickupAP-%s-%s.pdf' % (m, beforeAP))
            _figsize = (8, 6)
            fig = plt.figure(figsize=_figsize)
            fig.add_subplot(111)
            sns.barplot(x="hour", y=m, hue="year", data=dow_df)
            if m == 'percent':
                plt.ylim((0.0, 1.0))
            plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    hours = sorted(list(set(df.hour)))
    for i, beforeAP in enumerate(['beforeAPX', 'beforeAPO']):
        X, Y = [], []
        for h in hours:
            per2009 = df.loc[(df['beforeAP'] == i) & (df['year'] == 2009) & (df['hour'] == h)]['percent'].tolist().pop()
            per2010 = df.loc[(df['beforeAP'] == i) & (df['year'] == 2010) & (df['hour'] == h)]['percent'].tolist().pop()
            X.append(h)
            Y.append(per2010 - per2009)
        img_ofpath = opath.join(dpath['hourTrendPickupAP'], 'hourTrendPickupAP-%s-%s.pdf' % ('perDiff', beforeAP))
        fig = plt.figure(figsize=_figsize)
        fig.add_subplot(111)
        plt.plot(range(len(Y)), Y)
        plt.xticks(range(len(X)), X)
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)


def run_pickupAPQtime():
    m = 'QTime'
    #
    df = pd.read_csv(opath.join(dpath['_data'], 'pickupAP-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'pickupAP-2010.csv')))
    img_ofpath = opath.join(dpath['hourTrendPickupAP'], 'hourTrendPickupAP-%s.pdf' % m)
    _figsize = (8, 6)
    fig = plt.figure(figsize=_figsize)
    fig.add_subplot(111)
    sns.barplot(x="hour", y=m, hue="year", data=df)
    plt.ylim((0, 60))
    plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    dfX, dfO = df[(df['locPrevDropoff'] == 'X')], df[(df['locPrevDropoff'] != 'X')]
    for beforeAP, df_ in [('beforeAPX', dfX),
                          ('beforeAPO', dfO )]:
        img_ofpath = opath.join(dpath['hourTrendPickupAP'], 'hourTrendPickupAP-%s-%s.pdf' % (m, beforeAP))
        _figsize = (8, 6)
        fig = plt.figure(figsize=_figsize)
        fig.add_subplot(111)
        sns.barplot(x="hour", y=m, hue="year", data=df_)
        plt.ylim((0, 60))
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)


def run_pickupAPQNum():
    for yy in ['09', '10']:
        ifpath = opath.join(dpath['_data'], 'pickupAP-20%s.csv' % yy)
        
        
        csv_ofpath = opath.join(dpath['hourTrendPickupAP'], 'hourTrendPickupAPQNum-20%s.csv' % yy)
        #
        terminals = ['T1', 'T2', 'T3', 'BudgetT']
        labels = ['year', 'month', 'day', 'dow', 'hour', 'QNum', 'terminal']
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
                    records.append([year, month, day, dow, hour, QNum, tn])
        df = pd.DataFrame.from_records(records, columns=labels)
        df.to_csv(csv_ofpath, index=False)
        #
        img_ofpath = opath.join(dpath['hourTrendQNum'], 'hourTrendQNum-20%s.pdf' % yy)
        _figsize = (8, 6)
        fig = plt.figure(figsize=_figsize)
        fig.add_subplot(111)
        sns.barplot(x="hour", y="QNum", hue="terminal", data=df)
        plt.ylim((0, 100))
        plt.yticks(np.arange(0, 100, 20))
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    



def run_dropoffAPAfter():
    csv_ofpath = opath.join(dpath['hourTrendDropoffAPAfter'], 'hourTrendDropoffAPAfter.csv')
    labels = ['year', 'hour', 'afterAP', 'count', 'percent']
    records = []
    for yy in ['09', '10']:
        yyyy = int('20%s' % yy)
        df = pd.read_csv(opath.join(dpath['_data'], 'dropoffAP-20%s.csv' % yy))
        hour_wholeCount = {hour: count for hour, count in df.groupby(['hour']).count().reset_index()[['hour', 'did']].values}
        dfX, dfO = df[(df['locPickup'] == 'X')], df[(df['locPickup'] != 'X')]
        for i, df_ in enumerate([dfX, dfO]):
            groupby_df = df_.groupby(['hour']).count().reset_index()
            for hour, count in groupby_df[['hour', 'did']].values:
                records.append([yyyy, hour, i, count, count / float(hour_wholeCount[hour])])
    df = pd.DataFrame.from_records(records, columns=labels)
    df.to_csv(csv_ofpath, index=False)
    for i, afterAP in enumerate(['afterAPX', 'afterAPO']):
        dow_df = df[(df['afterAP'] == i)]
        for m in ['count', 'percent']:
            img_ofpath = opath.join(dpath['hourTrendDropoffAPAfter'], 'hourTrendDropoffAPAfter-%s-%s.pdf' % (m, afterAP))
            _figsize = (8, 6)
            fig = plt.figure(figsize=_figsize)
            fig.add_subplot(111)
            sns.barplot(x="hour", y=m, hue="year", data=dow_df)
            if m == 'percent':
                plt.ylim((0.0, 1.0))
            plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    hours = sorted(list(set(df.hour)))
    for i, afterAP in enumerate(['afterAPX', 'afterAPO']):
        X, Y = [], []
        for h in hours:
            per2009 = df.loc[(df['afterAP'] == i) & (df['year'] == 2009) & (df['hour'] == h)]['percent'].tolist().pop()
            per2010 = df.loc[(df['afterAP'] == i) & (df['year'] == 2010) & (df['hour'] == h)]['percent'].tolist().pop()
            X.append(h)
            Y.append(per2010 - per2009)
        img_ofpath = opath.join(dpath['hourTrendDropoffAPAfter'], 'hourTrendDropoffAPAfter-%s-%s.pdf' % ('perDiff', afterAP))
        fig = plt.figure(figsize=_figsize)
        ax = fig.add_subplot(111)
        plt.plot(range(len(Y)), Y)
        plt.xticks(range(len(X)), X)
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)


if __name__ == '__main__':
    run_numTrips()
    # run_pickupAPBefore()
    # run_dropoffAPAfter()
    # run_pickupAPQtime()
    # run_QNum()

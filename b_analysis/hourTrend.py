import __init__
from init_project import *
#
import pandas as pd
import seaborn as sns; sns.set_style("whitegrid")
import matplotlib.pyplot as plt
import numpy as np
import csv


_figsize = (8, 6)
_terminal_order = ['T1', 'T2', 'T3', 'BudgetT']

def run_numTrips():
    def process_numTrips_Wyear(_df, img_ofpath, ylimRange=None):
        hdf = _df.groupby(['year', 'month', 'day', 'hour']).count()['did'].to_frame('hourNumTrips').reset_index()
        yearHour_numTrips = {}
        hours = sorted(list(set(hdf['hour'])))
        for year, hour, numTrips in hdf.groupby(['year', 'hour']).mean()['hourNumTrips'].to_frame('hourAvgNumTrips').reset_index().values:
            yearHour_numTrips[year, hour] = numTrips
        fig = plt.figure(figsize=_figsize)
        ax = fig.add_subplot(111)
        ax.set_xlabel('hour')
        ax.set_ylabel('avgNumTrips')
        for year in [2009, 2010]:
            plt.plot(range(len(hours)), [yearHour_numTrips[year, hour] for hour in hours])
        plt.legend(['2009', '2010'], ncol=1, loc='upper left')
        plt.xticks(range(len(hours)), hours)
        if ylimRange:
            plt.ylim(ylimRange)
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    #
    def process_numTrips_Wdow(_df, img_ofpath):
        perHour_df = _df.groupby(['year', 'month', 'day', 'dow', 'hour']).count()['did'].to_frame('hourNumTrips').reset_index()
        dows, hours = set(), set()
        dowHour_numTrips = {}
        for dow, hour, numTrips in perHour_df.groupby(['dow', 'hour']).mean()['hourNumTrips'].to_frame('hourAvgNumTrips').reset_index().values:
            hour = int(hour)
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
        ax.set_ylabel('AvgNumTrips')
        for dow in dows:
            plt.plot(range(len(hours)), [dowHour_numTrips[dow, hour] for hour in hours])
        plt.legend(['Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat', 'Sun'], ncol=1, loc='upper left')
        plt.xticks(range(len(hours)), hours)
        plt.ylim((0, 1400))
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    df = pd.read_csv(opath.join(dpath['_data'], 'wholeAP-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'wholeAP-2010.csv')))
    #
    # img_ofpath = opath.join(dpath['hourNumTrips'], 'hourNumTripsWdow.pdf')
    # process_numTrips_Wdow(df, img_ofpath)
    # img_ofpath = opath.join(dpath['hourNumTrips'], 'hourNumTripsWyear.pdf')
    # process_numTrips_Wyear(df, img_ofpath)
    # #
    # img_ofpath = opath.join(dpath['hourNumTrips'], 'hourNumTripsWdowDropoff.pdf')
    # process_numTrips_Wdow(df[(df['locPrevDropoff'] != 'X')], img_ofpath)
    # img_ofpath = opath.join(dpath['hourNumTrips'], 'hourNumTripsWyearDropoff.pdf')
    # process_numTrips_Wyear(df[(df['locPrevDropoff'] != 'X')], img_ofpath)
    # for tn in ['T1', 'T2', 'T3', 'BudgetT']:
    #     img_ofpath = opath.join(dpath['hourNumTrips'], 'hourNumTripsWdowDropoff-%s.pdf' % tn)
    #     process_numTrips_Wdow(df[(df['locPrevDropoff'] == tn)], img_ofpath)
    #     img_ofpath = opath.join(dpath['hourNumTrips'], 'hourNumTripsWyearDropoff-%s.pdf' % tn)
    #     process_numTrips_Wyear(df[(df['locPrevDropoff'] == tn)], img_ofpath)
    # for year in [2009, 2010]:
    #     img_ofpath = opath.join(dpath['hourNumTrips'], 'hourNumTripsWdowDropoff-%d.pdf' % year)
    #     process_numTrips_Wdow(df[(df['locPrevDropoff'] != 'X') & (df['year'] == year)], img_ofpath)
    #     for tn in ['T1', 'T2', 'T3', 'BudgetT']:
    #         img_ofpath = opath.join(dpath['hourNumTrips'], 'hourNumTripsWdowDropoff-%d-%s.pdf' % (year, tn))
    #         process_numTrips_Wdow(df[(df['locPrevDropoff'] == tn) & (df['year'] == year)], img_ofpath)
    # #
    # img_ofpath = opath.join(dpath['hourNumTrips'], 'hourNumTripsWdowPickup.pdf')
    # process_numTrips_Wdow(df[(df['locPickup'] != 'X')], img_ofpath)
    # img_ofpath = opath.join(dpath['hourNumTrips'], 'hourNumTripsWyearPickup.pdf')
    # process_numTrips_Wyear(df[(df['locPickup'] != 'X')], img_ofpath)
    # for tn in ['T1', 'T2', 'T3', 'BudgetT']:
    #     img_ofpath = opath.join(dpath['hourNumTrips'], 'hourNumTripsWdowPickup-%s.pdf' % tn)
    #     process_numTrips_Wdow(df[(df['locPickup'] == tn)], img_ofpath)
    #     img_ofpath = opath.join(dpath['hourNumTrips'], 'hourNumTripsWyearPickup-%s.pdf' % tn)
    #     process_numTrips_Wyear(df[(df['locPickup'] == tn)], img_ofpath, (0, 300))
    # for year in [2009, 2010]:
    #     img_ofpath = opath.join(dpath['hourNumTrips'], 'hourNumTripsWdowPickup-%d.pdf' % year)
    #     process_numTrips_Wdow(df[(df['locPickup'] != 'X') & (df['year'] == year)], img_ofpath)
    #     for tn in ['T1', 'T2', 'T3', 'BudgetT']:
    #         img_ofpath = opath.join(dpath['hourNumTrips'], 'hourNumTripsWdowPickup-%d-%s.pdf' % (year, tn))
    #         process_numTrips_Wdow(df[(df['locPickup'] == tn) & (df['year'] == year)], img_ofpath)
    #
    # process_numTrips_Wterminal for pickupAP only
    #
    pickupAP_df = df[(df['locPickup'] != 'X')]
    pickupAP_df['terminal'] = pickupAP_df['locPickup']
    hdf = pickupAP_df.groupby(['year', 'month', 'day', 'hour', 'terminal']).count()['did'].to_frame('numTrips').reset_index()
    _figsize = (8, 6)
    fig = plt.figure(figsize=_figsize)
    fig.add_subplot(111)
    sns.barplot(x="hour", y="numTrips", hue="terminal", hue_order=_terminal_order, data=hdf)
    plt.ylim((0, 300))
    # plt.yticks(np.arange(0, 100, 20))
    img_ofpath = opath.join(dpath['hourNumTrips'], 'hourNumTripsWterminalPickup.pdf')
    plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)


def run_QTime():
    def process_QTime_Wterminal(_df, img_ofpath):
        _df['terminal'] = _df['locPickup']
        _figsize = (8, 6)
        fig = plt.figure(figsize=_figsize)
        fig.add_subplot(111)
        sns.barplot(x="hour", y="QTime", hue="terminal", hue_order=_terminal_order, data=_df)
        plt.ylim((0, 70))
        plt.yticks(np.arange(0, 70, 20))
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    #
    def process_QTime_Wyear(_df, img_ofpath):
        hdf = _df.groupby(['year', 'hour']).mean()['QTime'].to_frame('hourAvgQTime').reset_index()
        hours = sorted(list(set(hdf['hour'])))
        yearHour_QTime = {}
        for year, hour, QTime in hdf.values:
            yearHour_QTime[year, hour] = QTime
        fig = plt.figure(figsize=_figsize)
        ax = fig.add_subplot(111)
        ax.set_xlabel('hour')
        ax.set_ylabel('avgQTime')
        for year in [2009, 2010]:
            plt.plot(range(len(hours)), [yearHour_QTime[year, hour] for hour in hours])
        plt.legend(['2009', '2010'], ncol=1, loc='upper left')
        plt.xticks(range(len(hours)), hours)
        plt.ylim((0, 70))
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    #
    def process_QTime_Wdow(_df, img_ofpath):
        hdf = _df.groupby(['dow', 'hour']).mean()['QTime'].to_frame('hourAvgQTime').reset_index()
        dows, hours = set(), set()
        dowHour_numTrips = {}
        for dow, hour, QTime in hdf.values:
            hour = int(hour)
            dows.add(dow)
            hours.add(hour)
            dowHour_numTrips[dow, hour] = QTime
        dows, hours = map(sorted, map(list, [dows, hours]))
        fig = plt.figure(figsize=_figsize)
        ax = fig.add_subplot(111)
        ax.set_xlabel('hour')
        ax.set_ylabel('AvgQTime')
        for dow in dows:
            plt.plot(range(len(hours)), [dowHour_numTrips[dow, hour] for hour in hours])
        plt.legend(['Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat', 'Sun'], ncol=1, loc='upper left')
        plt.xticks(range(len(hours)), hours)
        plt.ylim((0, 70))
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)

    df = pd.read_csv(opath.join(dpath['_data'], 'pickupAP-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'pickupAP-2010.csv')))
    #
    # img_ofpath = opath.join(dpath['hourQTime'], 'hourQTimeWdow.pdf')
    # process_QTime_Wdow(df, img_ofpath)
    # img_ofpath = opath.join(dpath['hourQTime'], 'hourQTimeWyear.pdf')
    # process_QTime_Wyear(df, img_ofpath)
    img_ofpath = opath.join(dpath['hourQTime'], 'hourQTimeWterminal.pdf')
    process_QTime_Wterminal(df, img_ofpath)
    #
    # for tn in ['T1', 'T2', 'T3', 'BudgetT']:
    #     img_ofpath = opath.join(dpath['hourQTime'], 'hourQTimeWdow-%s.pdf' % tn)
    #     process_QTime_Wdow(df[(df['locPickup'] == tn)], img_ofpath)
    #     img_ofpath = opath.join(dpath['hourQTime'], 'hourQTimeWyear-%s.pdf' % tn)
    #     process_QTime_Wyear(df[(df['locPickup'] == tn)], img_ofpath)
    # for year in [2009, 2010]:
    #     img_ofpath = opath.join(dpath['hourQTime'], 'hourQTimeWdow-%d.pdf' % year)
    #     process_QTime_Wdow(df[(df['locPickup'] != 'X') & (df['year'] == year)], img_ofpath)
    #     for tn in ['T1', 'T2', 'T3', 'BudgetT']:
    #         img_ofpath = opath.join(dpath['hourQTime'], 'hourQTimeWdow-%d-%s.pdf' % (year, tn))
    #         process_QTime_Wdow(df[(df['locPickup'] == tn) & (df['year'] == year)], img_ofpath)


def run_QNum():
    def process_QNum_Wterminal(_df, img_ofpath):
        _figsize = (8, 6)
        fig = plt.figure(figsize=_figsize)
        fig.add_subplot(111)
        sns.barplot(x="hour", y="QNum", hue="terminal", hue_order=_terminal_order, data=_df)
        plt.ylim((0, 100))
        plt.yticks(np.arange(0, 100, 20))
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    #
    def process_QNum_Wyear(_df, img_ofpath):
        hdf = _df.groupby(['year', 'hour']).mean()['QNum'].to_frame('hourAvgQNum').reset_index()
        hours = sorted(list(set(hdf['hour'])))
        yearHour_QNum = {}
        for year, hour, QNum in hdf.values:
            yearHour_QNum[year, hour] = QNum
        fig = plt.figure(figsize=_figsize)
        ax = fig.add_subplot(111)
        ax.set_xlabel('hour')
        ax.set_ylabel('avgQNum')
        for year in [2009, 2010]:
            plt.plot(range(len(hours)), [yearHour_QNum[year, hour] for hour in hours])
        plt.legend(['2009', '2010'], ncol=1, loc='upper left')
        plt.xticks(range(len(hours)), hours)
        plt.ylim((0, 100))
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    #
    df = pd.read_csv(opath.join(dpath['_data'], 'wholeAP-QNum-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'wholeAP-QNum-2010.csv')))
    #
    img_ofpath = opath.join(dpath['hourQNum'], 'hourQNumWterminal.pdf')
    process_QNum_Wterminal(df, img_ofpath)
    for year in [2009, 2010]:
        img_ofpath = opath.join(dpath['hourQNum'], 'hourQNumWterminal-%d.pdf' % year)
        process_QNum_Wterminal(df[(df['year'] == year)], img_ofpath)
    img_ofpath = opath.join(dpath['hourQNum'], 'hourQNumWyear.pdf')
    process_QNum_Wyear(df, img_ofpath)
    for tn in ['T1', 'T2', 'T3', 'BudgetT']:
        img_ofpath = opath.join(dpath['hourQNum'], 'hourQNumWyear-%s.pdf' % (tn))
        process_QNum_Wyear(df[(df['terminal'] == tn)], img_ofpath)


def run_dropoffJoinP():
    def process_dropoffJoinP(_df, img_ofpath):
        hours = sorted(list(set(_df['hour'])))
        yearHour_percent = {}
        for year in [2009, 2010]:
            for hour in hours:
                sub_df = _df.loc[(_df['year'] == year) & (_df['hour'] == hour)]
                yearHour_percent[year, hour] = sub_df['J'].sum() / float(len(sub_df))
        #
        fig = plt.figure(figsize=_figsize)
        ax = fig.add_subplot(111)
        ax.set_xlabel('hour')
        ax.set_ylabel('percent')
        for year in [2009, 2010]:
            plt.plot(range(len(hours)), [yearHour_percent[year, hour] for hour in hours])
        plt.legend(['2009', '2010'], ncol=1, loc='upper left')
        plt.ylim((0.0, 1.0))
        plt.xticks(range(len(hours)), hours)

        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)

    df = pd.read_csv(opath.join(dpath['_data'], 'dropoffAP-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'dropoffAP-2010.csv')))
    #
    img_ofpath = opath.join(dpath['hourDropoffJoinP'], 'hourDropoffJoinP.pdf')
    process_dropoffJoinP(df, img_ofpath)
    #
    for tn in ['T1', 'T2', 'T3', 'BudgetT']:
        img_ofpath = opath.join(dpath['hourDropoffJoinP'], 'hourDropoffJoinP-%s.pdf' % tn)
        process_dropoffJoinP(df[(df['locPrevDropoff'] == tn)], img_ofpath)


def run_productivity():
    def process_productivity(_df, img_ofpath):
        hdf = _df.groupby(['J', 'hour']).mean()['productivity'].to_frame('hourAvgProductivity').reset_index()
        hours = sorted(list(set(hdf['hour'])))
        jHour_productivity = {}
        for j, hour, productivity in hdf.values:
            jHour_productivity[j, hour] = productivity
        fig = plt.figure(figsize=_figsize)
        ax = fig.add_subplot(111)
        ax.set_xlabel('hour')
        ax.set_ylabel('avgProductivity')
        for j in range(2):
            plt.plot(range(len(hours)), [jHour_productivity[j, hour] for hour in hours])
        plt.legend(['GO', 'GA'], ncol=1, loc='upper left')
        plt.xticks(range(len(hours)), hours)
        plt.ylim((10, 35))
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    #
    df = pd.read_csv(opath.join(dpath['_data'], 'dropoffAP-GA-hourProductivity-2009.csv'))
    for fn in ['dropoffAP-GA-hourProductivity-2010.csv',
               'dropoffAP-GO-hourProductivity-2009.csv',
               'dropoffAP-GO-hourProductivity-2010.csv']:
        df = df.append(pd.read_csv(opath.join(dpath['_data'], fn)))
    img_ofpath = opath.join(dpath['hourProductivity'], 'hourProductivity.pdf')
    process_productivity(df, img_ofpath)
    for year in [2009, 2010]:
        img_ofpath = opath.join(dpath['hourProductivity'], 'hourProductivity-%d.pdf' % year)
        process_productivity(df[(df['year'] == year)], img_ofpath)


if __name__ == '__main__':
    run_numTrips()
    # run_QTime()
    # run_dropoffJoinP()
    # run_QNum()
    # run_productivity()

import __init__
from __path_organizer import *
#
import pandas as pd
import seaborn as sns; sns.set_style("whitegrid")
import matplotlib.pyplot as plt
import numpy as np


def run_NTrip():
    def process_NTrip_Wyear(_df, img_ofpath, ylimRange=None):
        hdf = _df.groupby(['year', 'month', 'day', 'hour']).count()['did'].to_frame('hourNTrip').reset_index()
        yearHour_NTrip = {}
        hours = sorted(list(set(hdf['hour'])))
        for year, hour, NTrip in hdf.groupby(['year', 'hour']).mean()['hourNTrip'].to_frame('hourAvgNTrip').reset_index().values:
            yearHour_NTrip[year, hour] = NTrip
        fig = plt.figure(figsize=FIGSIZE)
        ax = fig.add_subplot(111)
        ax.set_xlabel('Hour')
        # ax.set_ylabel('avgNTrip')
        for i, year in enumerate([2009, 2010]):
            plt.plot(range(len(hours)), [yearHour_NTrip[year, hour] for hour in hours],
                     color=clists[i], marker=mlists[i])
        plt.legend(['2009', '2010'], ncol=1, loc='upper left')
        plt.xticks(range(len(hours)), hours)
        if ylimRange:
            plt.ylim(ylimRange)
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    #
    def process_NTrip_Wdow(_df, img_ofpath):
        perHour_df = _df.groupby(['year', 'month', 'day', 'dow', 'hour']).count()['did'].to_frame('hourNTrip').reset_index()
        dows, hours = set(), set()
        dowHour_NTrip = {}
        for dow, hour, NTrip in perHour_df.groupby(['dow', 'hour']).mean()['hourNTrip'].to_frame('hourAvgNTrip').reset_index().values:
            hour = int(hour)
            dows.add(dow)
            hours.add(hour)
            k = (dow, hour)
            if not dowHour_NTrip.has_key(k):
                dowHour_NTrip[k] = 0
            dowHour_NTrip[k] += NTrip
        dows, hours = map(sorted, map(list, [dows, hours]))
        fig = plt.figure(figsize=FIGSIZE)
        ax = fig.add_subplot(111)
        ax.set_xlabel('Hour')
        # ax.set_ylabel('AvgNTrip')
        for i, dow in enumerate(dows):
            plt.plot(range(len(hours)), [dowHour_NTrip[dow, hour] for hour in hours],
                     color=clists[i], marker=mlists[i])
        plt.legend(['Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat', 'Sun'], ncol=1, loc='upper left')
        plt.xticks(range(len(hours)), hours)
        plt.ylim((0, 1400))
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    df = pd.read_csv(opath.join(dpath['_data'], 'wholeAP-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'wholeAP-2010.csv')))
    #
    img_ofpath = opath.join(dpath['hourNTrip'], 'hourNTripWdow.pdf')
    process_NTrip_Wdow(df, img_ofpath)
    img_ofpath = opath.join(dpath['hourNTrip'], 'hourNTripWyear.pdf')
    process_NTrip_Wyear(df, img_ofpath)
    #
    img_ofpath = opath.join(dpath['hourNTrip'], 'hourNTripWdowDropoff.pdf')
    process_NTrip_Wdow(df[(df['locPrevDropoff'] != 'X')], img_ofpath)
    img_ofpath = opath.join(dpath['hourNTrip'], 'hourNTripWyearDropoff.pdf')
    process_NTrip_Wyear(df[(df['locPrevDropoff'] != 'X')], img_ofpath)
    for tn in ['T1', 'T2', 'T3', 'BudgetT']:
        img_ofpath = opath.join(dpath['hourNTrip'], 'hourNTripWdowDropoff-%s.pdf' % tn)
        process_NTrip_Wdow(df[(df['locPrevDropoff'] == tn)], img_ofpath)
        img_ofpath = opath.join(dpath['hourNTrip'], 'hourNTripWyearDropoff-%s.pdf' % tn)
        process_NTrip_Wyear(df[(df['locPrevDropoff'] == tn)], img_ofpath)
    for year in [2009, 2010]:
        img_ofpath = opath.join(dpath['hourNTrip'], 'hourNTripWdowDropoff-%d.pdf' % year)
        process_NTrip_Wdow(df[(df['locPrevDropoff'] != 'X') & (df['year'] == year)], img_ofpath)
        for tn in ['T1', 'T2', 'T3', 'BudgetT']:
            img_ofpath = opath.join(dpath['hourNTrip'], 'hourNTripWdowDropoff-%d-%s.pdf' % (year, tn))
            process_NTrip_Wdow(df[(df['locPrevDropoff'] == tn) & (df['year'] == year)], img_ofpath)
    #
    img_ofpath = opath.join(dpath['hourNTrip'], 'hourNTripWdowPickup.pdf')
    process_NTrip_Wdow(df[(df['locPickup'] != 'X')], img_ofpath)
    img_ofpath = opath.join(dpath['hourNTrip'], 'hourNTripWyearPickup.pdf')
    process_NTrip_Wyear(df[(df['locPickup'] != 'X')], img_ofpath)
    for tn in ['T1', 'T2', 'T3', 'BudgetT']:
        img_ofpath = opath.join(dpath['hourNTrip'], 'hourNTripWdowPickup-%s.pdf' % tn)
        process_NTrip_Wdow(df[(df['locPickup'] == tn)], img_ofpath)
        img_ofpath = opath.join(dpath['hourNTrip'], 'hourNTripWyearPickup-%s.pdf' % tn)
        process_NTrip_Wyear(df[(df['locPickup'] == tn)], img_ofpath, (0, 300))
    for year in [2009, 2010]:
        img_ofpath = opath.join(dpath['hourNTrip'], 'hourNTripWdowPickup-%d.pdf' % year)
        process_NTrip_Wdow(df[(df['locPickup'] != 'X') & (df['year'] == year)], img_ofpath)
        for tn in ['T1', 'T2', 'T3', 'BudgetT']:
            img_ofpath = opath.join(dpath['hourNTrip'], 'hourNTripWdowPickup-%d-%s.pdf' % (year, tn))
            process_NTrip_Wdow(df[(df['locPickup'] == tn) & (df['year'] == year)], img_ofpath)
    #
    # process_NTrip_Wterminal for pickupAP only
    #
    pickupAP_df = df[(df['locPickup'] != 'X')]
    pickupAP_df['terminal'] = pickupAP_df['locPickup']
    hdf = pickupAP_df.groupby(['year', 'month', 'day', 'hour', 'terminal']).count()['did'].to_frame('NTrip').reset_index()
    figsize = (8, 6)
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    sns.barplot(x="hour", y="NTrip", hue="terminal", hue_order=terminal_order, data=hdf)
    ax.set_xlabel('Hour')
    ax.set_ylabel('')
    plt.ylim((0, 300))
    # plt.yticks(np.arange(0, 100, 20))
    img_ofpath = opath.join(dpath['hourNTrip'], 'hourNTripWterminalPickup.pdf')
    plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)


def run_QTime():
    def process_QTime_Wterminal(_df, img_ofpath):
        _df['terminal'] = _df['locPickup']
        figsize = (8, 6)
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
        sns.barplot(x="hour", y="QTime", hue="terminal", hue_order=terminal_order, data=_df)
        ax.set_xlabel('Hour')
        ax.set_ylabel('Minutes')
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
        fig = plt.figure(figsize=FIGSIZE)
        ax = fig.add_subplot(111)
        ax.set_xlabel('Hour')
        ax.set_ylabel('Minutes')
        for i, year in enumerate([2009, 2010]):
            plt.plot(range(len(hours)), [yearHour_QTime[year, hour] for hour in hours],
                     color=clists[i], marker=mlists[i])
        plt.legend(['2009', '2010'], ncol=1, loc='upper left')
        plt.xticks(range(len(hours)), hours)
        plt.ylim((0, 70))
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    #
    def process_QTime_Wdow(_df, img_ofpath):
        hdf = _df.groupby(['dow', 'hour']).mean()['QTime'].to_frame('hourAvgQTime').reset_index()
        dows, hours = set(), set()
        dowHour_NTrip = {}
        for dow, hour, QTime in hdf.values:
            hour = int(hour)
            dows.add(dow)
            hours.add(hour)
            dowHour_NTrip[dow, hour] = QTime
        dows, hours = map(sorted, map(list, [dows, hours]))
        fig = plt.figure(figsize=FIGSIZE)
        ax = fig.add_subplot(111)
        ax.set_xlabel('Hour')
        ax.set_ylabel('Minutes')
        for i, dow in enumerate(dows):
            print(img_ofpath)
            print(dow, [dowHour_NTrip[dow, hour] for hour in hours])
            print()
            plt.plot(range(len(hours)), [dowHour_NTrip[dow, hour] for hour in hours],
                     color=clists[i], marker=mlists[i])
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
    # img_ofpath = opath.join(dpath['hourQTime'], 'hourQTimeWterminal.pdf')
    # process_QTime_Wterminal(df, img_ofpath)
    # #
    # for tn in ['T1', 'T2', 'T3', 'BudgetT']:
    #     img_ofpath = opath.join(dpath['hourQTime'], 'hourQTimeWdow-%s.pdf' % tn)
    #     process_QTime_Wdow(df[(df['locPickup'] == tn)], img_ofpath)
    #     img_ofpath = opath.join(dpath['hourQTime'], 'hourQTimeWyear-%s.pdf' % tn)
    #     process_QTime_Wyear(df[(df['locPickup'] == tn)], img_ofpath)
    for year in [2009, 2010]:
        img_ofpath = opath.join(dpath['hourQTime'], 'hourQTimeWdow-%d.pdf' % year)
        process_QTime_Wdow(df[(df['locPickup'] != 'X') & (df['year'] == year)], img_ofpath)
        # for tn in ['T1', 'T2', 'T3', 'BudgetT']:
        #     img_ofpath = opath.join(dpath['hourQTime'], 'hourQTimeWdow-%d-%s.pdf' % (year, tn))
        #     process_QTime_Wdow(df[(df['locPickup'] == tn) & (df['year'] == year)], img_ofpath)


def run_QNum():
    def process_QNum_Wterminal(_df, img_ofpath):
        fig = plt.figure(figsize=FIGSIZE)
        fig.add_subplot(111)
        ax = fig.add_subplot(111)
        sns.barplot(x="hour", y="QNum", hue="terminal", hue_order=terminal_order, data=_df)
        ax.set_xlabel('Hour')
        ax.set_ylabel('')
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
        fig = plt.figure(figsize=FIGSIZE)
        ax = fig.add_subplot(111)
        ax.set_xlabel('Hour')
        # ax.set_ylabel('avgQNum')
        for i, year in enumerate([2009, 2010]):
            plt.plot(range(len(hours)), [yearHour_QNum[year, hour] for hour in hours],
                     color=clists[i], marker=mlists[i])
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


def run_QRatio():
    def process_QRatio(_df, img_ofpath):
        hours = sorted(list(set(_df['hour'])))
        yearHour_percent = {}
        for year in [2009, 2010]:
            for hour in hours:
                sub_df = _df.loc[(_df['year'] == year) & (_df['hour'] == hour)]
                yearHour_percent[year, hour] = (sub_df['GA'].sum() / float(len(sub_df))) * 100
        #
        fig = plt.figure(figsize=FIGSIZE)
        ax = fig.add_subplot(111)
        ax.set_xlabel('Hour')
        ax.set_ylabel('%')
        for i, year in enumerate([2009, 2010]):
            plt.plot(range(len(hours)), [yearHour_percent[year, hour] for hour in hours],
                     color=clists[i], marker=mlists[i])
        plt.legend(['2009', '2010'], ncol=1, loc='upper left')
        plt.ylim((0, 100))
        plt.xticks(range(len(hours)), hours)

        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)

    df = pd.read_csv(opath.join(dpath['_data'], 'dropoffAP-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'dropoffAP-2010.csv')))
    #
    img_ofpath = opath.join(dpath['hourQRatio'], 'hourQRatio.pdf')
    process_QRatio(df, img_ofpath)
    #
    for tn in ['T1', 'T2', 'T3', 'BudgetT']:
        img_ofpath = opath.join(dpath['hourQRatio'], 'hourQRatio-%s.pdf' % tn)
        process_QRatio(df[(df['locPrevDropoff'] == tn)], img_ofpath)


def run_productivity():
    def process_productivity(_df, img_ofpath):
        hdf = _df.groupby(['GA', 'hour']).mean()['productivity'].to_frame('hourAvgProductivity').reset_index()
        hours = sorted(list(set(hdf['hour'])))
        jHour_productivity = {}
        for i, hour, productivity in hdf.values:
            jHour_productivity[i, hour] = productivity
        fig = plt.figure(figsize=FIGSIZE)
        ax = fig.add_subplot(111)
        ax.set_xlabel('Hour')
        ax.set_ylabel('S$ / Hour')
        for i in range(2):
            plt.plot(range(len(hours)), [jHour_productivity[i, hour] for hour in hours],
                     color=clists[i], marker=mlists[i])
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
    run_NTrip()
    run_QTime()
    # run_QNum()
    # run_productivity()
    # run_QRatio()


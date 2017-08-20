import __init__
from init_project import *
#
import seaborn as sns; sns.set_style("whitegrid")
import pandas as pd
import matplotlib.pyplot as plt


def run_NTrip():
    def process_NTrip_Wyear(_df, img_ofpath, ylimRange=None):
        mdf = _df.groupby(['year', 'month']).count()['did'].to_frame('monthNTrip').reset_index()
        month2009 = set(mdf[(mdf['year'] == 2009)]['month'])
        month2010 = set(mdf[(mdf['year'] == 2010)]['month'])
        bothYearMonth = sorted(list(month2009.intersection(month2010)))
        mdf = mdf.drop(mdf[~(mdf['month'].isin(bothYearMonth))].index)
        yearMonth_NTrip = {}
        for year, month, NTrip in mdf.values:
            k = (year, month)
            if not yearMonth_NTrip.has_key(k):
                yearMonth_NTrip[k] = 0
            yearMonth_NTrip[k] += NTrip
        fig = plt.figure(figsize=FIGSIZE)
        ax = fig.add_subplot(111)
        ax.set_xlabel('Month')
        ax.set_ylabel('SumNTrip')
        for i, year in enumerate([2009, 2010]):
            plt.plot(range(len(bothYearMonth)), [yearMonth_NTrip[year, month] for month in bothYearMonth],
                     color=clists[i], marker=mlists[i])
        plt.legend(['2009', '2010'], ncol=1, loc='upper left')
        plt.xticks(range(len(bothYearMonth)), bothYearMonth)
        if ylimRange:
            plt.ylim(ylimRange)
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    df = pd.read_csv(opath.join(dpath['_data'], 'wholeAP-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'wholeAP-2010.csv')))
    #
    img_ofpath = opath.join(dpath['monthNTrip'], 'monthNTrip.pdf')
    process_NTrip_Wyear(df, img_ofpath)

    img_ofpath = opath.join(dpath['monthNTrip'], 'monthNTripPickup.pdf')
    process_NTrip_Wyear(df[(df['locPickup'] != 'X')], img_ofpath)
    for tn in ['T1', 'T2', 'T3', 'BudgetT']:
        img_ofpath = opath.join(dpath['monthNTrip'], 'monthNTripPickup-%s.pdf' % tn)
        process_NTrip_Wyear(df[(df['locPickup'] == tn)], img_ofpath, (10000, 80000))

    img_ofpath = opath.join(dpath['monthNTrip'], 'monthNTripDropoff.pdf')
    process_NTrip_Wyear(df[(df['locPrevDropoff'] != 'X')], img_ofpath)
    for tn in ['T1', 'T2', 'T3', 'BudgetT']:
        img_ofpath = opath.join(dpath['monthNTrip'], 'monthNTripDropoff-%s.pdf' % tn)
        process_NTrip_Wyear(df[(df['locPrevDropoff'] == tn)], img_ofpath, (18000, 120000))


def run_QTime():
    def process_Qtime(_df, img_ofpath):
        mdf = _df.groupby(['year', 'month']).mean()['QTime'].to_frame('avgQtime').reset_index()
        month2009 = set(mdf[(mdf['year'] == 2009)]['month'])
        month2010 = set(mdf[(mdf['year'] == 2010)]['month'])
        bothYearMonth = sorted(list(month2009.intersection(month2010)))
        mdf = mdf.drop(mdf[~(mdf['month'].isin(bothYearMonth))].index)
        yearMonth_NTrip = {}
        for year, month, NTrip in mdf.values:
            k = (year, month)
            if not yearMonth_NTrip.has_key(k):
                yearMonth_NTrip[k] = 0
            yearMonth_NTrip[k] += NTrip
        fig = plt.figure(figsize=FIGSIZE)
        ax = fig.add_subplot(111)
        ax.set_xlabel('Month')
        ax.set_ylabel('AvgQTime')
        for i, year in enumerate([2009, 2010]):
            plt.plot(range(len(bothYearMonth)), [yearMonth_NTrip[year, month] for month in bothYearMonth],
                     color=clists[i], marker=mlists[i])
        plt.legend(['2009', '2010'], ncol=1, loc='upper left')
        plt.xticks(range(len(bothYearMonth)), bothYearMonth)
        plt.ylim((0, 40))
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    df = pd.read_csv(opath.join(dpath['_data'], 'pickupAP-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'pickupAP-2010.csv')))
    #
    img_ofpath = opath.join(dpath['monthQTime'], 'monthQTime.pdf')
    process_Qtime(df, img_ofpath)
    for tn in ['T1', 'T2', 'T3', 'BudgetT']:
        img_ofpath = opath.join(dpath['monthQTime'], 'monthQTime-%s.pdf' % tn)
        process_Qtime(df[(df['locPickup'] == tn)], img_ofpath)


def run_QRatio():
    def process_QRatio(_df, img_ofpath):
        month2009 = set(_df[(_df['year'] == 2009)]['month'])
        month2010 = set(_df[(_df['year'] == 2010)]['month'])
        bothYearMonth = sorted(list(month2009.intersection(month2010)))
        _df = _df.drop(_df[~(_df['month'].isin(bothYearMonth))].index)
        #
        months = sorted(list(bothYearMonth))
        yearMonth_percent = {}
        for year in [2009, 2010]:
            for month in months:
                sub_df = _df.loc[(_df['year'] == year) & (_df['month'] == month)]
                yearMonth_percent[year, month] = (sub_df['GA'].sum() / float(len(sub_df))) * 100
        #
        fig = plt.figure(figsize=FIGSIZE)
        ax = fig.add_subplot(111)
        ax.set_xlabel('Month')
        ax.set_ylabel('%')
        for i, year in enumerate([2009, 2010]):
            plt.plot(range(len(months)), [yearMonth_percent[year, month] for month in months],
                     color=clists[i], marker=mlists[i])
        plt.legend(['2009', '2010'], ncol=1, loc='upper left')
        plt.ylim((0, 100))
        plt.xticks(range(len(months)), months)
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    #
    df = pd.read_csv(opath.join(dpath['_data'], 'dropoffAP-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'dropoffAP-2010.csv')))
    #
    img_ofpath = opath.join(dpath['monthQRatio'], 'monthQRatio.pdf')
    process_QRatio(df, img_ofpath)
    for tn in ['T1', 'T2', 'T3', 'BudgetT']:
        img_ofpath = opath.join(dpath['monthQRatio'], 'monthQRatio-%s.pdf' % tn)
        process_QRatio(df[(df['locPrevDropoff'] == tn)], img_ofpath)

if __name__ == '__main__':
    # run_NTrip()
    # run_QTime()
    run_QRatio()
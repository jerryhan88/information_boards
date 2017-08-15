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
    def process_numTrips_Wyear(_df, img_ofpath):
        mdf = _df.groupby(['year', 'month']).count()['did'].to_frame('monthNumTrips').reset_index()
        month2009 = set(mdf[(mdf['year'] == 2009)]['month'])
        month2010 = set(mdf[(mdf['year'] == 2010)]['month'])
        bothYearMonth = sorted(list(month2009.intersection(month2010)))
        mdf = mdf.drop(mdf[~(mdf['month'].isin(bothYearMonth))].index)
        yearMonth_numTrips = {}
        for year, month, numTrips in mdf.values:
            k = (year, month)
            if not yearMonth_numTrips.has_key(k):
                yearMonth_numTrips[k] = 0
            yearMonth_numTrips[k] += numTrips
        fig = plt.figure(figsize=_figsize)
        ax = fig.add_subplot(111)
        ax.set_xlabel('month')
        ax.set_ylabel('SumNumTrips')
        for year in [2009, 2010]:
            plt.plot(range(len(bothYearMonth)), [yearMonth_numTrips[year, month] for month in bothYearMonth])
        plt.legend(['2009', '2010'], ncol=1, loc='upper left')
        plt.xticks(range(len(bothYearMonth)), bothYearMonth)
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    df = pd.read_csv(opath.join(dpath['_data'], 'wholeAP-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'wholeAP-2010.csv')))
    #
    img_ofpath = opath.join(dpath['monthNumTrips'], 'monthNumTrips.pdf')
    process_numTrips_Wyear(df, img_ofpath)
    #
    img_ofpath = opath.join(dpath['monthNumTrips'], 'monthNumTripsDropoff.pdf')
    process_numTrips_Wyear(df[(df['locPrevDropoff'] != 'X')], img_ofpath)
    for tn in ['T1', 'T2', 'T3', 'BudgetT']:
        img_ofpath = opath.join(dpath['monthNumTrips'], 'monthNumTripsDropoff-%s.pdf' % tn)
        process_numTrips_Wyear(df[(df['locPrevDropoff'] == tn)], img_ofpath)
    img_ofpath = opath.join(dpath['monthNumTrips'], 'monthNumTripsPickup.pdf')
    process_numTrips_Wyear(df[(df['locPickup'] != 'X')], img_ofpath)
    for tn in ['T1', 'T2', 'T3', 'BudgetT']:
        img_ofpath = opath.join(dpath['monthNumTrips'], 'monthNumTripsPickup-%s.pdf' % tn)
        process_numTrips_Wyear(df[(df['locPickup'] == tn)], img_ofpath)


def run_QTime():
    def process_Qtime(_df, img_ofpath):
        mdf = _df.groupby(['year', 'month']).mean()['QTime'].to_frame('avgQtime').reset_index()
        month2009 = set(mdf[(mdf['year'] == 2009)]['month'])
        month2010 = set(mdf[(mdf['year'] == 2010)]['month'])
        bothYearMonth = sorted(list(month2009.intersection(month2010)))
        mdf = mdf.drop(mdf[~(mdf['month'].isin(bothYearMonth))].index)
        yearMonth_numTrips = {}
        for year, month, numTrips in mdf.values:
            k = (year, month)
            if not yearMonth_numTrips.has_key(k):
                yearMonth_numTrips[k] = 0
            yearMonth_numTrips[k] += numTrips
        fig = plt.figure(figsize=_figsize)
        ax = fig.add_subplot(111)
        ax.set_xlabel('month')
        ax.set_ylabel('AvgQTime')
        for year in [2009, 2010]:
            plt.plot(range(len(bothYearMonth)), [yearMonth_numTrips[year, month] for month in bothYearMonth])
        plt.legend(['2009', '2010'], ncol=1, loc='upper left')
        plt.xticks(range(len(bothYearMonth)), bothYearMonth)
        plt.ylim((0, 40))
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    df = pd.read_csv(opath.join(dpath['_data'], 'pickupAP-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'pickupAP-2010.csv')))
    #
    img_ofpath = opath.join(dpath['monthAvgQTime'], 'monthAvgQTime.pdf')
    process_Qtime(df, img_ofpath)
    for tn in ['T1', 'T2', 'T3', 'BudgetT']:
        img_ofpath = opath.join(dpath['monthAvgQTime'], 'monthAvgQTime-%s.pdf' % tn)
        process_Qtime(df[(df['locPickup'] == tn)], img_ofpath)


def run_dropoffJoinP():
    df = pd.read_csv(opath.join(dpath['_data'], 'dropoffAP-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'dropoffAP-2010.csv')))
    month2009 = set(df[(df['year'] == 2009)]['month'])
    month2010 = set(df[(df['year'] == 2010)]['month'])
    bothYearMonth = sorted(list(month2009.intersection(month2010)))
    df = df.drop(df[~(df['month'].isin(bothYearMonth))].index)
    #
    months = sorted(list(bothYearMonth))
    yearMonth_percent = {}
    for year in [2009, 2010]:
        for month in months:
            sub_df = df.loc[(df['year'] == year) & (df['month'] == month)]
            yearMonth_percent[year, month] = sub_df['J'].sum() / float(len(sub_df))
    #
    fig = plt.figure(figsize=_figsize)
    ax = fig.add_subplot(111)
    ax.set_xlabel('month')
    ax.set_ylabel('percent')
    for year in [2009, 2010]:
        plt.plot(range(len(months)), [yearMonth_percent[year, month] for month in months])
    plt.legend(['2009', '2010'], ncol=1, loc='upper left')
    plt.ylim((0.0, 1.0))
    plt.xticks(range(len(months)), months)
    img_ofpath = opath.join(dpath['monthDropoffJoinP'], 'monthDropoffJoinP.pdf')
    plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)


if __name__ == '__main__':
    run_numTrips()
    # run_QTime()
    # run_dropoffJoinP()
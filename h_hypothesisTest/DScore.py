import __init__
from __path_organizer import *
#
import pandas as pd
import seaborn as sns; sns.set_style("whitegrid")
import matplotlib.pyplot as plt


def process_hourPlots(df, img_ofpath, ylimRange=None):
    hdf = df.groupby(['year', 'hour']).mean()['DScore'].to_frame('avgDScore').reset_index()
    hours = sorted(list(set(hdf['hour'])))
    yearHour_QTime = {}
    for year, hour, DScore in hdf.values:
        yearHour_QTime[year, hour] = DScore
    fig = plt.figure(figsize=FIGSIZE)
    ax = fig.add_subplot(111)
    ax.set_xlabel('Hour')
    for i, year in enumerate([2009, 2010]):
        plt.plot(range(len(hours)), [yearHour_QTime[year, hour] for hour in hours],
                 color=clists[i], marker=mlists[i])
    plt.legend(['2009', '2010'], ncol=1, loc='upper left')
    plt.xticks(range(len(hours)), hours)
    plt.ylim(ylimRange)
    plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)


def process_monthPlots(df, img_ofpath, ylimRange=None):
    mdf = df.groupby(['year', 'month']).mean()['DScore'].to_frame('avgDScore').reset_index()
    month2009 = set(mdf[(mdf['year'] == 2009)]['month'])
    month2010 = set(mdf[(mdf['year'] == 2010)]['month'])
    bothYearMonth = sorted(list(month2009.intersection(month2010)))
    mdf = mdf.drop(mdf[~(mdf['month'].isin(bothYearMonth))].index)
    yearMonth_NTrip = {}
    for year, month, NTrip in mdf.values:
        yearMonth_NTrip[year, month] = NTrip
    fig = plt.figure(figsize=FIGSIZE)
    ax = fig.add_subplot(111)
    ax.set_xlabel('Month')
    for i, year in enumerate([2009, 2010]):
        plt.plot(range(len(bothYearMonth)), [yearMonth_NTrip[year, month] for month in bothYearMonth],
                 color=clists[i], marker=mlists[i])
    plt.legend(['2009', '2010'], ncol=1, loc='upper left')
    plt.xticks(range(len(bothYearMonth)), bothYearMonth)
    plt.ylim(ylimRange)
    plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)


def run_pickupAP():
    df = pd.read_csv(opath.join(dpath['_data'], 'pickupAP-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'pickupAP-2010.csv')))
    #
    img_ofpath = opath.join(dpath['hypDScore'], 'hypDScore-pickupAP-hour.pdf')
    process_hourPlots(df, img_ofpath, (0, 3))
    img_ofpath = opath.join(dpath['hypDScore'], 'hypDScore-pickupAP-month.pdf')
    process_monthPlots(df, img_ofpath, (0, 3))


def run_dropoffAP():
    df = pd.read_csv(opath.join(dpath['_data'], 'dropoffAP-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'dropoffAP-2010.csv')))

    img_ofpath = opath.join(dpath['hypDScore'], 'hypDScore-dropoffAP-hour.pdf')
    process_hourPlots(df, img_ofpath, (-4, 4))
    img_ofpath = opath.join(dpath['hypDScore'], 'hypDScore-dropoffAP-month.pdf')
    process_monthPlots(df, img_ofpath, (0, 2))


def run_dropoffXAP():
    df = pd.read_csv(opath.join(dpath['_data'], 'dropoffXAP-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'dropoffXAP-2010.csv')))

    img_ofpath = opath.join(dpath['hypDScore'], 'hypDScore-dropoffXAP-hour.pdf')
    process_hourPlots(df, img_ofpath, (-4, 4))
    img_ofpath = opath.join(dpath['hypDScore'], 'hypDScore-dropoffXAP-month.pdf')
    process_monthPlots(df, img_ofpath, (0, 2))


if __name__ == '__main__':
    # run_pickupAP()
    run_dropoffAP()
    # run_dropoffXAP()
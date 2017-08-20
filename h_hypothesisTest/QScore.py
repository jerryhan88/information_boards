import __init__
from init_project import *
#
import pandas as pd
import seaborn as sns; sns.set_style("whitegrid")
import matplotlib.pyplot as plt


def process_hourPlots(df, img_ofpath):
    hdf = df.groupby(['year', 'hour']).mean()['QScore'].to_frame('avgQScore').reset_index()
    hours = sorted(list(set(hdf['hour'])))
    yearHour_QTime = {}
    for year, hour, QScore in hdf.values:
        yearHour_QTime[year, hour] = QScore
    fig = plt.figure(figsize=FIGSIZE)
    ax = fig.add_subplot(111)
    ax.set_xlabel('Hour')
    for i, year in enumerate([2009, 2010]):
        plt.plot(range(len(hours)), [yearHour_QTime[year, hour] for hour in hours],
                 color=clists[i], marker=mlists[i])
    plt.legend(['2009', '2010'], ncol=1, loc='upper left')
    plt.xticks(range(len(hours)), hours)
    plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)

def process_monthPlots(df, img_ofpath):
    mdf = df.groupby(['year', 'month']).mean()['QScore'].to_frame('avgQScore').reset_index()
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
    plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)


def run_pickupAP():
    df = pd.read_csv(opath.join(dpath['_data'], 'pickupAP-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'pickupAP-2010.csv')))
    #
    img_ofpath = opath.join(dpath['hypQScore'], 'hypQScore-pickupAP-hour.pdf')
    process_hourPlots(df, img_ofpath)
    img_ofpath = opath.join(dpath['hypQScore'], 'hypQScore-pickupAP-month.pdf')
    process_monthPlots(df, img_ofpath)


def run_dropoffAP():
    df = pd.read_csv(opath.join(dpath['_data'], 'dropoffAP-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'dropoffAP-2010.csv')))

    img_ofpath = opath.join(dpath['hypQScore'], 'hypQScore-dropoffAP-hour.pdf')
    process_hourPlots(df, img_ofpath)
    img_ofpath = opath.join(dpath['hypQScore'], 'hypQScore-dropoffAP-month.pdf')
    process_monthPlots(df, img_ofpath)


if __name__ == '__main__':
    # run_pickupAP()
    run_dropoffAP()
import __init__
from init_project import *
#
from scipy.stats import ttest_ind
import pandas as pd
import csv


stats = [
         'avg2009', 'avg2010',
         'diff',
         'num2009', 'num2010',
         'std2009', 'std2009',
         'tScore', 'pValue']


def no_fixed():
    df2009, df2010 = map(pd.read_csv,
                         [opath.join(dpath['analysis'], 'ap-dropoff-pickup-2009.csv'),
                          opath.join(dpath['analysis'], 'ap-dropoff-pickup-2010.csv')])
    dv = 'QTime'
    ofpath = opath.join(dpath['dropoffAP_pickupAP_tTest'], 'no_fixed_%s.csv' % dv)
    with open(ofpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(stats)
    #
    num2009, num2010 = map(len, [df2009, df2010])
    mean2009, mean2010 = df2009[dv].mean(), df2010[dv].mean()
    std2009, std2010 = df2009[dv].std(), df2010[dv].std()
    t, p = ttest_ind(df2009[dv], df2010[dv])
    with open(ofpath, 'a') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow([
                         mean2009, mean2010,
                         mean2009 - mean2010,
                         num2009, num2010,
                         std2009, std2010,
                         t, p])


def dow_fixed():
    df2009, df2010 = map(pd.read_csv,
                         [opath.join(dpath['analysis'], 'ap-dropoff-pickup-2009.csv'),
                          opath.join(dpath['analysis'], 'ap-dropoff-pickup-2010.csv')])
    dv = 'QTime'
    ofpath = opath.join(dpath['dropoffAP_pickupAP_tTest'], 'dow_fixed_%s.csv' % dv)
    with open(ofpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(['dow'] + stats)
    #
    dows = list(set(df2009['dow']).intersection(set(df2010['dow'])))
    dows.sort()
    for w in dows:
        dow_df2009 = df2009[(df2009['dow'] == w)]
        dow_df2010 = df2010[(df2010['dow'] == w)]
        num2009, num2010 = map(len, [dow_df2009, dow_df2010])
        mean2009, mean2010 = dow_df2009[dv].mean(), dow_df2010[dv].mean()
        std2009, std2010 = dow_df2009[dv].std(), dow_df2010[dv].std()
        t, p = ttest_ind(dow_df2009[dv], dow_df2010[dv])
        with open(ofpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow([w,
                             mean2009, mean2010,
                             mean2009 - mean2010,
                             num2009, num2010,
                             std2009, std2010,
                             t, p])


def month_fixed():
    df2009, df2010 = map(pd.read_csv,
                         [opath.join(dpath['analysis'], 'ap-dropoff-pickup-2009.csv'),
                          opath.join(dpath['analysis'], 'ap-dropoff-pickup-2010.csv')])
    dv = 'QTime'
    ofpath = opath.join(dpath['dropoffAP_pickupAP_tTest'], 'month_fixed_%s.csv' % dv)
    with open(ofpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(['month'] + stats)
    #
    months = list(set(df2009['month']).intersection(set(df2010['month'])))
    months.sort()
    for m in months:
        month_df2009 = df2009[(df2009['month'] == m)]
        month_df2010 = df2010[(df2010['month'] == m)]
        num2009, num2010 = map(len, [month_df2009, month_df2010])
        mean2009, mean2010 = month_df2009[dv].mean(), month_df2010[dv].mean()
        std2009, std2010 = month_df2009[dv].std(), month_df2010[dv].std()
        t, p = ttest_ind(month_df2009[dv], month_df2010[dv])
        with open(ofpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow([m,
                             mean2009, mean2010,
                             mean2009 - mean2010,
                             num2009, num2010,
                             std2009, std2010,
                             t, p])


def hour_fixed():
    df2009, df2010 = map(pd.read_csv,
                         [opath.join(dpath['analysis'], 'ap-dropoff-pickup-2009.csv'),
                          opath.join(dpath['analysis'], 'ap-dropoff-pickup-2010.csv')])
    dv = 'QTime'
    ofpath = opath.join(dpath['dropoffAP_pickupAP_tTest'], 'hour_fixed_%s.csv' % dv)
    with open(ofpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(['hour'] + stats)
    #
    hours = list(set(df2009['hour']).intersection(set(df2010['hour'])))
    hours.sort()
    for h in hours:
        hour_df2009 = df2009[(df2009['hour'] == h)]
        hour_df2010 = df2010[(df2010['hour'] == h)]
        num2009, num2010 = map(len, [hour_df2009, hour_df2010])
        mean2009, mean2010 = hour_df2009[dv].mean(), hour_df2010[dv].mean()
        std2009, std2010 = hour_df2009[dv].std(), hour_df2010[dv].std()
        t, p = ttest_ind(hour_df2009[dv], hour_df2010[dv])
        with open(ofpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow([h,
                             mean2009, mean2010,
                             mean2009 - mean2010,
                             num2009, num2010,
                             std2009, std2010,
                             t, p])


def driver_fixed():
    df2009, df2010 = map(pd.read_csv,
                         [opath.join(dpath['analysis'], 'ap-dropoff-pickup-2009.csv'),
                          opath.join(dpath['analysis'], 'ap-dropoff-pickup-2010.csv')])
    dv = 'QTime'
    ofpath = opath.join(dpath['dropoffAP_pickupAP_tTest'], 'driver_fixed_%s.csv' % dv)
    with open(ofpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(['did'] + stats)
    #
    drivers = list(set(df2009['did']).intersection(set(df2010['did'])))
    drivers.sort()
    for did in drivers:
        did_df2009 = df2009[(df2009['did'] == did)]
        did_df2010 = df2010[(df2010['did'] == did)]
        num2009, num2010 = map(len, [did_df2009, did_df2010])
        mean2009, mean2010 = did_df2009[dv].mean(), did_df2010[dv].mean()
        std2009, std2010 = did_df2009[dv].std(), did_df2010[dv].std()
        t, p = ttest_ind(did_df2009[dv], did_df2010[dv])
        with open(ofpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow([did,
                             mean2009, mean2010,
                             mean2009 - mean2010,
                             num2009, num2010,
                             std2009, std2010,
                             t, p])


def month_driver_fixed():
    df2009, df2010 = map(pd.read_csv,
                         [opath.join(dpath['analysis'], 'ap-dropoff-pickup-2009.csv'),
                          opath.join(dpath['analysis'], 'ap-dropoff-pickup-2010.csv')])
    dv = 'QTime'
    months = list(set(df2009['month']).intersection(set(df2010['month'])))
    months.sort()
    ofpath = opath.join(dpath['dropoffAP_pickupAP_tTest'], 'month_driver_fixed_%s.csv' % dv)
    with open(ofpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(['month', 'did'] + stats)
    for m in months:
        month_df2009 = df2009[(df2009['month'] == m)]
        month_df2010 = df2010[(df2010['month'] == m)]
        drivers = list(set(month_df2009['did']).intersection(set(month_df2010['did'])))
        drivers.sort()
        for did in drivers:
            month_did_df2009 = month_df2009[(month_df2009['did'] == did)]
            month_did_df2010 = month_df2010[(month_df2010['did'] == did)]
            num2009, num2010 = map(len, [month_did_df2009, month_did_df2010])
            mean2009, mean2010 = month_did_df2009[dv].mean(), month_did_df2010[dv].mean()
            std2009, std2010 = month_did_df2009[dv].std(), month_did_df2010[dv].std()
            t, p = ttest_ind(month_did_df2009[dv], month_did_df2010[dv])
            with open(ofpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow([m, did,
                                 mean2009, mean2010,
                                 mean2009 - mean2010,
                                 num2009, num2010,
                                 std2009, std2010,
                                 t, p])


if __name__ == '__main__':
    no_fixed()
import b_analysis
from init_project import *
#
import pandas as pd
import numpy as np
import statsmodels.api as sm
import csv


def run():
    pickAP_filtering_summary_fpath = opath.join(dpath['analysis'], 'readMe (pickupAP_filtering).txt')
    dropoffRegression_fpath =opath.join(dpath['6_dropoffRegression'], 'dropoffRegressionResults.csv')
    with open(dropoffRegression_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        new_header = ['year', 'month', 'coef', 'const',
                      'p_coef', 'p_const']
        writer.writerow(new_header)
    with open(pickAP_filtering_summary_fpath, 'a') as f:
        f.write("This document include contents about filtering criteria and the number of instances. ")
        f.write("File's name starts with 'pickupAP' and the following number represent year. ")
        f.write("These files include only trip instance that drivers pick up passenger at the airport.")
        f.write("Also, some trip instances whose date belongs to weekend and public holidays are firstly removed.\n")
        f.write("The followings show criteria for filtering outliers;\n")
        f.write("\t O1. QTime < 0 or QTime >= 180 minutes\n")
        f.write("\t O2. Productivity > 80 S$ / hour \n")
        f.write("\t O3. Duration < 1 minute \n")
        f.write("\n")

    for yy in ['09', '10']:
        ofpath = opath.join(dpath['analysis'], 'pickupAP-20%s.csv' % yy)
        year = int('20%s' % yy)
        holidays = HOLIDAYS2009 if yy == '09' else HOLIDAYS2010
        with open(pickAP_filtering_summary_fpath, 'a') as f:
            f.write('The summary of 20%s data filtering\n' % yy)
        ifpath = opath.join(dpath['analysis'], 'whole-ap-20%s.csv' % yy)
        df = pd.read_csv(ifpath)
        df = df[(df['pickUpTerminal'] != 'X')]
        df['weekday'] = df.apply(lambda row: 0 if ((row['year'], row['month'], row['day']) in holidays) or
                                                  (row['dow'] in WEEKENDS) else 1, axis=1)
        df = df[(df['weekday'] == 1)]
        with open(pickAP_filtering_summary_fpath, 'a') as f:
            f.write('Before filtering\n')
            f.write('\t The number of instance: %d\n' % len(df))
        #
        Qtime_outLowerBound = set(np.where(df['qrTime'] <= TH_QRTIME_MIN)[0])
        Qtime_outUpperBound = set(np.where(df['qrTime'] > TH_QRTIME_MAX)[0])
        QTime_ol = Qtime_outLowerBound.union(Qtime_outUpperBound)
        productivity_ol = set(np.where(df['productivity'] > TH_PRODUCTIVITY)[0])
        duration_ol = set(np.where(df['duration'] <= TH_DURATION)[0])
        outlier_index = QTime_ol.union(productivity_ol)
        outlier_index = outlier_index.union(duration_ol)
        with open(pickAP_filtering_summary_fpath, 'a') as f:
            f.write('The number of outliers\n')
            f.write('\t # of outliers: %d (%.3f %%)\n' % (len(outlier_index),
                                                    100 * len(outlier_index) / float(len(df))))
            f.write('\t\t # of O1: %d (%.3f %%)\n' % (len(QTime_ol),
                                               100 * len(QTime_ol) / float(len(df))))
            f.write('\t\t # of O2: %d (%.3f %%)\n' % (len(productivity_ol),
                                               100 * len(productivity_ol) / float(len(df))))
            f.write('\t\t # of O3: %d (%.3f %%)\n' % (len(duration_ol),
                                               100 * len(duration_ol) / float(len(df))))
        #
        df = df.drop(df.index[list(outlier_index)])
        with open(pickAP_filtering_summary_fpath, 'a') as f:
            f.write('After filtering\n')
            f.write('\t The number of instance: %d\n' % len(df))
            f.write('\n')
        #
        terminals = set(['BudgetT', 'T1', 'T2', 'T3'])
        df['X'] = df.apply(lambda row: 1 if row['prevEndTerminal'] in terminals else 0, axis=1)
        df.to_csv(ofpath, index=False)
        months = list(set(df['month']))
        months.sort()
        for m in months:
            month_df = df[(df['month'] == m)]
            y = month_df['qrTime']
            X = month_df[['X']]
            X = sm.add_constant(X)
            res = sm.OLS(y, X, missing='drop').fit()
            with open(dropoffRegression_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow([year, m, res.params['X'], res.params['const'],
                                 res.pvalues['X'], res.pvalues['const']])

if __name__ == '__main__':
    run()

#
# df['weekday'] = df.apply(lambda row : 0 if ((row['year'], row['month'], row['day']) in holidays) or
#                                            (row['dow'] in WEEKENDS) else 1, axis=1)
# dummiesM = []
# for m in set(df['month']):
#     month_str = 'M%d' % m
#     df[month_str] = np.where(df['month'] == m, 1, 0)
#     dummiesM.append(month_str)
#
# dummiesH = []
# for h in set(df['hour']):
#     hour_str = 'H%d' % h
#     df[hour_str] = np.where(df['hour'] == h, 1, 0)
#     dummiesH.append(hour_str)
#
# dummiesW = []
# for w in set(df['weekday']):
#     weekday_str = 'W%d' % w
#     df[weekday_str] = np.where(df['weekday'] == w, 1, 0)
#     dummiesW.append(weekday_str)
#
# #
# # Filtering
# #
#
# df['qrTime'].hist()
# df[(df['qrTime'] <= TH_QRTIME_MAX) & (df['qrTime'] > TH_QRTIME_MIN)]['qrTime'].hist()
#
#
# Qtime_outLowerBound = set(np.where(df['qrTime'] <= TH_QRTIME_MIN)[0])
# Qtime_outUpperBound = set(np.where(df['qrTime'] > TH_QRTIME_MAX)[0])
# QTime_outliers = Qtime_outLowerBound.union(Qtime_outUpperBound)
# productivity_outliers = set(np.where(df['productivity'] > TH_PRODUCTIVITY)[0])
# duration_outliers = set(np.where(df['duration'] <= TH_DURATION)[0])
#
# outlier_index = QTime_outliers.union(productivity_outliers)
# outlier_index = outlier_index.union(duration_outliers)
#
# df = df.drop(df.index[list(outlier_index)])
#
# df['qrTime'].hist()
#
# df = df[['qrTime', 'X'] + dummiesM + dummiesH + dummiesW]
#
# df.columns = [['QTime', 'X'] + dummiesM + dummiesH + dummiesW]
#
#
# df.to_csv('temp1.csv', index=False)
#
#
#
#
# y = df['QTime']
# X = df[['X'] + dummiesM[:-1] + dummiesH[:-1] + dummiesW[:-1]]
# X = sm.add_constant(X)
# res = sm.OLS(y, X, missing='drop').fit()
# res.summary()
#
# df[(df['X'] == 1)]['QTime'].hist()
# df[(df['X'] == 0)]['QTime'].hist()
# df[(df['X'] == 1)]['QTime'].mean(), df[(df['X'] == 1)]['QTime'].std()
# df[(df['X'] == 0)]['QTime'].mean(), df[(df['X'] == 0)]['QTime'].std()

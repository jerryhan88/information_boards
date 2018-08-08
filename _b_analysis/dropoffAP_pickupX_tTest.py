import h_hypothesisTest
from __path_organizer import *
#
import sys
import itertools
from scipy.stats import ttest_ind
import pandas as pd
import csv


stats = [
         'avg2009', 'avg2010',
         'diff',
         'num2009', 'num2010',
         'std2009', 'std2009',
         'tScore', 'pValue']


flag_FE = {
    'w': 'dow',
    'm': 'month',
    'h': 'hour',
    'd': 'did'
}

df2009, df2010 = map(pd.read_csv,
                     [opath.join(dpath['analysis'], 'dropoffAP-pickupX-2009.csv'),
                      opath.join(dpath['analysis'], 'dropoffAP-pickupX-2010.csv')])

dv = 'durTillPickup'


def do_tTest_wf(fixedEffects):
    if fixedEffects == 'X':
        ofpath = opath.join(dpath['dropoffAP_pickupX_tTest'], 'X_%s_tTest.csv' % dv)
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
    else:
        ofpath = opath.join(dpath['dropoffAP_pickupX_tTest'], '%s_%s_tTest.csv' % (fixedEffects, dv))
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = []
            for fe in fixedEffects:
                header.append(flag_FE[fe])
            header += stats
            writer.writerow(header)
        fixedEffects = [flag_FE[fe] for fe in fixedEffects]
        dummy_indices = []
        for fe in fixedEffects:
            indices = list(set(df2009[fe]).intersection(set(df2010[fe])))
            indices.sort()
            dummy_indices.append(indices)
        for di in sorted(list(itertools.product(*dummy_indices))):
            subset_df2009, subset_df2010 = df2009, df2010
            for i, fe in enumerate(fixedEffects):
                subset_df2009 = subset_df2009[(subset_df2009[fe] == di[i])]
                subset_df2010 = subset_df2010[(subset_df2010[fe] == di[i])]
            num2009, num2010 = map(len, [subset_df2009, subset_df2010])
            mean2009, mean2010 = subset_df2009[dv].mean(), subset_df2010[dv].mean()
            std2009, std2010 = subset_df2009[dv].std(), subset_df2010[dv].std()
            t, p = ttest_ind(subset_df2009[dv], subset_df2010[dv])
            with open(ofpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_row = list(di)
                new_row += [ mean2009, mean2010,
                             mean2009 - mean2010,
                             num2009, num2010,
                             std2009, std2010,
                             t, p]
                writer.writerow(new_row)


if __name__ == '__main__':
    args = sys.argv
    assert len(args) == len(['pyFile', 'fixedEffects'])
    _, fixedEffects = args
    do_tTest_wf(fixedEffects)
    # no_fixed()
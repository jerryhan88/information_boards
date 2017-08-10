import __init__
from init_project import *
#
import sys
import itertools
import statsmodels.api as sm
import pandas as pd
import csv


flag_measures = {
    'Q': 'QTime',
    'I': 'durTillPickup',
    'P': 'productivity'
}

flag_FE = {
    'w': 'dow',
    'm': 'month',
    'h': 'hour',
    'd': 'did'
}


def regression_wf(fixedEffects, measure):
    assert fixedEffects
    df2009, df2010 = map(pd.read_csv,
                         [opath.join(dpath['analysis'], 'ap-pickup-2009.csv'),
                          opath.join(dpath['analysis'], 'ap-pickup-2010.csv')])
    dv = flag_measures[measure]
    ofpath = opath.join(dpath['pickupAP_Regression'], '%s_%s.csv' % (fixedEffects, dv))
    with open(ofpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = ['year']
        for fe in fixedEffects:
            header.append(flag_FE[fe])
        header += ['numObs', 'numJoins', 'ratio_X',
                   'coef_X', 'const', 'p_X', 'p_const',
                   'p_f', 'R2']
        writer.writerow(header)
    #
    fixedEffects = [flag_FE[fe] for fe in fixedEffects]
    for year, df in [(2009, df2009), (2010, df2010)]:
        dummy_indices = []
        for fe in fixedEffects:
            indices = list(set(df[fe]))
            indices.sort()
            dummy_indices.append(indices)
        for di in list(itertools.product(*dummy_indices)):
            subset_df = df
            for i, fe in enumerate(fixedEffects):
                subset_df = subset_df[(subset_df[fe] == di[i])]
            if len(subset_df) < 2:
                    continue
            try:
                y = subset_df[dv]
                X = subset_df[['X']]
                X = sm.add_constant(X)
                res = sm.OLS(y, X, missing='drop').fit()
                numObs, numJoins = len(subset_df), subset_df['X'].sum()
                ratio_X = numJoins / float(numObs)
                with open(ofpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    new_row = [year]
                    new_row += list(di)
                    new_row += [numObs, numJoins, ratio_X,
                                res.params['X'], res.params['const'], res.pvalues['X'], res.pvalues['const'], 
                                res.f_pvalue, res.rsquared]
                    writer.writerow(new_row)
                
            except:
                continue


def no_fixed():
    df2009, df2010 = map(pd.read_csv,
                         [opath.join(dpath['analysis'], 'ap-pickup-2009.csv'),
                          opath.join(dpath['analysis'], 'ap-pickup-2010.csv')])
    for dv in ['QTime', 'durTillPickup', 'productivity']:
        ofpath = opath.join(dpath['pickupAP_Regression'], 'no_fixed_%s.csv' % dv)
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['year', 'numObs', 'ratio_X',
                             'coef_X', 'const', 'p_X', 'p_const',
                             'p_f', 'R2'])
        for year, df in [(2009, df2009), (2010, df2010)]:
            ratio_x = df['X'].sum() / float(len(df))
            if not(0.05 < ratio_x < 0.95):
                continue
            y = df[dv]
            X = df[['X']]
            X = sm.add_constant(X)
            res = sm.OLS(y, X, missing='drop').fit()
            with open(ofpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow([year, len(df), ratio_x,
                                 res.params['X'], res.params['const'],
                                 res.pvalues['X'], res.pvalues['const'], res.f_pvalue, res.rsquared])



if __name__ == '__main__':
    args = sys.argv
    assert len(args) == len(['pyFile', 'fixedEffects', 'measure'])
    _, fixedEffects, measure = args
    regression_wf(fixedEffects, measure)

    # no_fixed()

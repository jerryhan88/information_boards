import __init__
from init_project import *
#
import statsmodels.api as sm
import pandas as pd
import csv


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


def dow_fixed():
    df2009, df2010 = map(pd.read_csv,
                         [opath.join(dpath['analysis'], 'ap-pickup-2009.csv'),
                          opath.join(dpath['analysis'], 'ap-pickup-2010.csv')])
    for dv in ['QTime', 'durTillPickup', 'productivity']:
        ofpath = opath.join(dpath['pickupAP_Regression'], 'dow_fixed_%s.csv' % dv)
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['year', 'month', 'numObs', 'ratio_X',
                             'coef_X', 'const', 'p_X', 'p_const',
                             'p_f', 'R2'])
        for year, df in [(2009, df2009), (2010, df2010)]:
            dows = list(set(df['dow']))
            dows.sort()
            for w in dows:
                dow_df = df[(df['dow'] == w)]
                if len(dow_df) < 2:
                    continue
                ratio_x = dow_df['X'].sum() / float(len(dow_df))
                if not (0.05 < ratio_x < 0.95):
                    continue
                try:
                    y = dow_df[dv]
                    X = dow_df[['X']]
                    X = sm.add_constant(X)
                    res = sm.OLS(y, X, missing='drop').fit()
                    with open(ofpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        writer.writerow([year, w, len(dow_df), ratio_x,
                                         res.params['X'], res.params['const'],
                                         res.pvalues['X'], res.pvalues['const'], res.f_pvalue, res.rsquared])
                except:
                    continue


def month_fixed():
    df2009, df2010 = map(pd.read_csv,
                         [opath.join(dpath['analysis'], 'ap-pickup-2009.csv'),
                          opath.join(dpath['analysis'], 'ap-pickup-2010.csv')])
    for dv in ['QTime', 'durTillPickup', 'productivity']:
        ofpath = opath.join(dpath['pickupAP_Regression'], 'month_fixed_%s.csv' % dv)
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['year', 'month', 'numObs', 'ratio_X',
                             'coef_X', 'const', 'p_X', 'p_const',
                             'p_f', 'R2'])
        for year, df in [(2009, df2009), (2010, df2010)]:
            months = list(set(df['month']))
            months.sort()
            for m in months:
                month_df = df[(df['month'] == m)]
                if len(month_df) < 2:
                    continue
                ratio_x = month_df['X'].sum() / float(len(month_df))
                if not (0.05 < ratio_x < 0.95):
                    continue
                try:
                    y = month_df[dv]
                    X = month_df[['X']]
                    X = sm.add_constant(X)
                    res = sm.OLS(y, X, missing='drop').fit()
                    with open(ofpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        writer.writerow([year, m, len(month_df), ratio_x,
                                         res.params['X'], res.params['const'],
                                         res.pvalues['X'], res.pvalues['const'], res.f_pvalue, res.rsquared])
                except:
                    continue


def hour_fixed():
    df2009, df2010 = map(pd.read_csv,
                         [opath.join(dpath['analysis'], 'ap-pickup-2009.csv'),
                          opath.join(dpath['analysis'], 'ap-pickup-2010.csv')])
    for dv in ['QTime', 'durTillPickup', 'productivity']:
        ofpath = opath.join(dpath['pickupAP_Regression'], 'hour_fixed_%s.csv' % dv)
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['year', 'hour', 'numObs', 'ratio_X',
                             'coef_X', 'const', 'p_X', 'p_const',
                             'p_f', 'R2'])
        for year, df in [(2009, df2009), (2010, df2010)]:
            hours = list(set(df['hour']))
            hours.sort()
            for h in hours:
                hour_df = df[(df['hour'] == h)]
                if len(hour_df) < 2:
                    continue
                ratio_x = hour_df['X'].sum() / float(len(hour_df))
                if not (0.05 < ratio_x < 0.95):
                    continue
                try:
                    y = hour_df[dv]
                    X = hour_df[['X']]
                    X = sm.add_constant(X)
                    res = sm.OLS(y, X, missing='drop').fit()
                    with open(ofpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        writer.writerow([year, h, len(hour_df), ratio_x,
                                         res.params['X'], res.params['const'],
                                         res.pvalues['X'], res.pvalues['const'], res.f_pvalue, res.rsquared])
                except:
                    continue


def driver_fixed():
    df2009, df2010 = map(pd.read_csv,
                         [opath.join(dpath['analysis'], 'ap-pickup-2009.csv'),
                          opath.join(dpath['analysis'], 'ap-pickup-2010.csv')])
    for dv in ['QTime', 'durTillPickup', 'productivity']:
        ofpath = opath.join(dpath['pickupAP_Regression'], 'driver_fixed_%s.csv' % dv)
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['year', 'did', 'numObs', 'ratio_X',
                             'coef_X', 'const', 'p_X', 'p_const',
                             'p_f', 'R2'])
        for year, df in [(2009, df2009), (2010, df2010)]:
            drivers = list(set(df['did']))
            drivers.sort()
            for did in drivers:
                did_df = df[(df['did'] == did)]
                if len(did_df) < 2:
                    continue
                ratio_x = did_df['X'].sum() / float(len(did_df))
                if not (0.05 < ratio_x < 0.95):
                    continue
                try:
                    y = did_df[dv]
                    X = did_df[['X']]
                    X = sm.add_constant(X)
                    res = sm.OLS(y, X, missing='drop').fit()
                    with open(ofpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        writer.writerow([year, did, len(did_df), ratio_x,
                                         res.params['X'], res.params['const'],
                                         res.pvalues['X'], res.pvalues['const'], res.f_pvalue, res.rsquared])
                except:
                    continue


def hour_month_fixed():
    df2009, df2010 = map(pd.read_csv,
                         [opath.join(dpath['analysis'], 'ap-pickup-2009.csv'),
                          opath.join(dpath['analysis'], 'ap-pickup-2010.csv')])
    for dv in ['QTime', 'durTillPickup', 'productivity']:
        ofpath = opath.join(dpath['pickupAP_Regression'], 'hour_month_fixed_%s.csv' % dv)
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['year', 'hour', 'month', 'numObs', 'ratio_X',
                             'coef_X', 'const', 'p_X', 'p_const',
                             'p_f', 'R2'])
        for year, df in [(2009, df2009), (2010, df2010)]:
            hours = list(set(df['hour']))
            hours.sort()
            for h in hours:
                hour_df = df[(df['hour'] == h)]
                months = list(set(hour_df['month']))
                months.sort()
                for m in months:
                    hour_month_df = hour_df[(hour_df['month'] == m)]
                    if len(hour_month_df) < 2:
                        continue
                    ratio_x = hour_month_df['X'].sum() / float(len(hour_month_df))
                    if not (0.05 < ratio_x < 0.95):
                        continue
                    try:
                        y = hour_month_df[dv]
                        X = hour_month_df[['X']]
                        X = sm.add_constant(X)
                        res = sm.OLS(y, X, missing='drop').fit()
                        with open(ofpath, 'a') as w_csvfile:
                            writer = csv.writer(w_csvfile, lineterminator='\n')
                            writer.writerow([year, h, m, len(hour_month_df), ratio_x,
                                             res.params['X'], res.params['const'],
                                             res.pvalues['X'], res.pvalues['const'], res.f_pvalue, res.rsquared])
                    except:
                        continue


def hour_dow_fixed():
    df2009, df2010 = map(pd.read_csv,
                         [opath.join(dpath['analysis'], 'ap-pickup-2009.csv'),
                          opath.join(dpath['analysis'], 'ap-pickup-2010.csv')])
    for dv in ['QTime', 'durTillPickup', 'productivity']:
        ofpath = opath.join(dpath['pickupAP_Regression'], 'hour_dow_fixed_%s.csv' % dv)
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['year', 'hour', 'dow', 'numObs', 'ratio_X',
                             'coef_X', 'const', 'p_X', 'p_const',
                             'p_f', 'R2'])
        for year, df in [(2009, df2009), (2010, df2010)]:
            hours = list(set(df['hour']))
            hours.sort()
            for h in hours:
                hour_df = df[(df['hour'] == h)]
                dows = list(set(hour_df['dow']))
                dows.sort()
                for w in dows:
                    hour_dow_df = hour_df[(hour_df['dow'] == w)]
                    if len(hour_dow_df) < 2:
                        continue
                    ratio_x = hour_dow_df['X'].sum() / float(len(hour_dow_df))
                    if not (0.05 < ratio_x < 0.95):
                        continue
                    try:
                        y = hour_dow_df[dv]
                        X = hour_dow_df[['X']]
                        X = sm.add_constant(X)
                        res = sm.OLS(y, X, missing='drop').fit()
                        with open(ofpath, 'a') as w_csvfile:
                            writer = csv.writer(w_csvfile, lineterminator='\n')
                            writer.writerow([year, h, w, len(hour_dow_df), ratio_x,
                                             res.params['X'], res.params['const'],
                                             res.pvalues['X'], res.pvalues['const'], res.f_pvalue, res.rsquared])
                    except:
                        continue


def hour_driver_fixed():
    df2009, df2010 = map(pd.read_csv,
                         [opath.join(dpath['analysis'], 'ap-pickup-2009.csv'),
                          opath.join(dpath['analysis'], 'ap-pickup-2010.csv')])
    for dv in ['QTime', 'durTillPickup', 'productivity']:
        ofpath = opath.join(dpath['pickupAP_Regression'], 'hour_driver_fixed_%s.csv' % dv)
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['year', 'hour', 'did', 'numObs', 'ratio_X',
                             'coef_X', 'const', 'p_X', 'p_const',
                             'p_f', 'R2'])
        for year, df in [(2009, df2009), (2010, df2010)]:
            hours = list(set(df['hour']))
            hours.sort()
            for h in hours:
                hour_df = df[(df['hour'] == h)]
                drivers = list(set(hour_df['did']))
                drivers.sort()
                for did in drivers:
                    hour_did_df = hour_df[(hour_df['did'] == did)]
                    if len(hour_did_df) < 2:
                        continue
                    ratio_x = hour_did_df['X'].sum() / float(len(hour_did_df))
                    if not (0.05 < ratio_x < 0.95):
                        continue
                    try:
                        y = hour_did_df[dv]
                        X = hour_did_df[['X']]
                        X = sm.add_constant(X)
                        res = sm.OLS(y, X, missing='drop').fit()
                        with open(ofpath, 'a') as w_csvfile:
                            writer = csv.writer(w_csvfile, lineterminator='\n')
                            writer.writerow([year, h, did, len(hour_did_df), ratio_x,
                                             res.params['X'], res.params['const'],
                                             res.pvalues['X'], res.pvalues['const'], res.f_pvalue, res.rsquared])
                    except:
                        continue


def hour_month_dow_fixed():
    df2009, df2010 = map(pd.read_csv,
                         [opath.join(dpath['analysis'], 'ap-pickup-2009.csv'),
                          opath.join(dpath['analysis'], 'ap-pickup-2010.csv')])
    for dv in ['QTime', 'durTillPickup', 'productivity']:
        ofpath = opath.join(dpath['pickupAP_Regression'], 'hour_month_dow_fixed_%s.csv' % dv)
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['year', 'hour', 'month', 'dow', 'numObs', 'ratio_X',
                             'coef_X', 'const', 'p_X', 'p_const',
                             'p_f', 'R2'])
        for year, df in [(2009, df2009), (2010, df2010)]:
            hours = list(set(df['hour']))
            hours.sort()
            for h in hours:
                hour_df = df[(df['hour'] == h)]
                months = list(set(hour_df['month']))
                months.sort()
                for m in months:
                    hour_month_df = hour_df[(hour_df['month'] == m)]
                    dows = list(set(hour_month_df['dow']))
                    dows.sort()
                    for w in dows:
                        hour_month_dow_df = hour_month_df[(hour_month_df['dow'] == w)]
                        if len(hour_month_dow_df) < 2:
                            continue
                        ratio_x = hour_month_dow_df['X'].sum() / float(len(hour_month_dow_df))
                        if not (0.05 < ratio_x < 0.95):
                            continue
                        try:
                            y = hour_month_dow_df[dv]
                            X = hour_month_dow_df[['X']]
                            X = sm.add_constant(X)
                            res = sm.OLS(y, X, missing='drop').fit()
                            with open(ofpath, 'a') as w_csvfile:
                                writer = csv.writer(w_csvfile, lineterminator='\n')
                                writer.writerow([year, h, m, w, len(hour_month_dow_df), ratio_x,
                                                 res.params['X'], res.params['const'],
                                                 res.pvalues['X'], res.pvalues['const'], res.f_pvalue, res.rsquared])
                        except:
                            continue


def hour_month_did_fixed():
    df2009, df2010 = map(pd.read_csv,
                         [opath.join(dpath['analysis'], 'ap-pickup-2009.csv'),
                          opath.join(dpath['analysis'], 'ap-pickup-2010.csv')])
    for dv in ['QTime', 'durTillPickup', 'productivity']:
        ofpath = opath.join(dpath['pickupAP_Regression'], 'hour_month_did_fixed_%s.csv' % dv)
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['year', 'hour', 'month', 'did', 'numObs', 'ratio_X',
                             'coef_X', 'const', 'p_X', 'p_const',
                             'p_f', 'R2'])
        for year, df in [(2009, df2009), (2010, df2010)]:
            hours = list(set(df['hour']))
            hours.sort()
            for h in hours:
                hour_df = df[(df['hour'] == h)]
                months = list(set(hour_df['month']))
                months.sort()
                for m in months:
                    hour_month_df = hour_df[(hour_df['month'] == m)]
                    drivers = list(set(hour_month_df['did']))
                    drivers.sort()
                    for did in drivers:
                        hour_month_did_df = hour_month_df[(hour_month_df['did'] == did)]
                        if len(hour_month_did_df) < 2:
                            continue
                        ratio_x = hour_month_did_df['X'].sum() / float(len(hour_month_did_df))
                        if not (0.05 < ratio_x < 0.95):
                            continue
                        try:
                            y = hour_month_did_df[dv]
                            X = hour_month_did_df[['X']]
                            X = sm.add_constant(X)
                            res = sm.OLS(y, X, missing='drop').fit()
                            with open(ofpath, 'a') as w_csvfile:
                                writer = csv.writer(w_csvfile, lineterminator='\n')
                                writer.writerow([year, h, m, did, len(hour_month_did_df), ratio_x,
                                                 res.params['X'], res.params['const'],
                                                 res.pvalues['X'], res.pvalues['const'], res.f_pvalue, res.rsquared])
                        except:
                            continue




def hour_month_dow_did_fixed():
    df2009, df2010 = map(pd.read_csv,
                         [opath.join(dpath['analysis'], 'ap-pickup-2009.csv'),
                          opath.join(dpath['analysis'], 'ap-pickup-2010.csv')])
    for dv in ['QTime', 'durTillPickup', 'productivity']:
        ofpath = opath.join(dpath['pickupAP_Regression'], 'hour_month_dow_did_fixed_%s.csv' % dv)
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['year', 'hour', 'month', 'dow', 'did', 'numObs', 'ratio_X',
                             'coef_X', 'const', 'p_X', 'p_const',
                             'p_f', 'R2'])
        for year, df in [(2009, df2009), (2010, df2010)]:
            hours = list(set(df['hour']))
            hours.sort()
            for h in hours:
                hour_df = df[(df['hour'] == h)]
                months = list(set(hour_df['month']))
                months.sort()
                for m in months:
                    hour_month_df = hour_df[(hour_df['month'] == m)]
                    dows = list(set(hour_month_df['dow']))
                    dows.sort()
                    for w in dows:
                        hour_month_dow_df = hour_month_df[(hour_month_df['dow'] == w)]
                        drivers = list(set(hour_month_df['did']))
                        drivers.sort()
                        for did in drivers:
                            hour_month_dow_did_df = hour_month_dow_df[(hour_month_dow_df['did'] == did)]
                            if len(hour_month_dow_did_df) < 2:
                                continue
                            ratio_x = hour_month_dow_did_df['X'].sum() / float(len(hour_month_dow_did_df))
                            if not (0.05 < ratio_x < 0.95):
                                continue
                            try:
                                y = hour_month_dow_did_df[dv]
                                X = hour_month_dow_did_df[['X']]
                                X = sm.add_constant(X)
                                res = sm.OLS(y, X, missing='drop').fit()
                                with open(ofpath, 'a') as w_csvfile:
                                    writer = csv.writer(w_csvfile, lineterminator='\n')
                                    writer.writerow([year, h, m, w, did, len(hour_month_dow_did_df), ratio_x,
                                                     res.params['X'], res.params['const'],
                                                     res.pvalues['X'], res.pvalues['const'], res.f_pvalue, res.rsquared])
                            except:
                                continue


def month_driver_fixed():
    df2009, df2010 = map(pd.read_csv,
                         [opath.join(dpath['analysis'], 'ap-pickup-2009.csv'),
                          opath.join(dpath['analysis'], 'ap-pickup-2010.csv')])
    for dv in ['QTime', 'durTillPickup', 'productivity']:
        ofpath = opath.join(dpath['pickupAP_Regression'], 'month_driver_fixed_%s.csv' % dv)
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['year', 'month', 'did',
                             'numObs', 'ratio_X',
                             'coef_X', 'const', 'p_X', 'p_const',
                             'p_f', 'R2'])
        for year, df in [(2009, df2009), (2010, df2010)]:
            months = list(set(df['month']))
            months.sort()
            for m in months:
                month_df = df[(df['month'] == m)]
                drivers = list(set(month_df['did']))
                drivers.sort()
                for did in drivers:
                    month_did_df = month_df[(month_df['did'] == did)]
                    if len(month_did_df) < 2:
                        continue
                    ratio_x = month_did_df['X'].sum() / float(len(month_did_df))
                    if not (0.05 < ratio_x < 0.95):
                        continue
                    try:
                        y = month_did_df[dv]
                        X = month_did_df[['X']]
                        X = sm.add_constant(X)
                        res = sm.OLS(y, X, missing='drop').fit()
                        with open(ofpath, 'a') as w_csvfile:
                            writer = csv.writer(w_csvfile, lineterminator='\n')
                            writer.writerow([year, m, did,
                                             len(month_did_df), ratio_x,
                                             res.params['X'], res.params['const'],
                                             res.pvalues['X'], res.pvalues['const'], res.f_pvalue, res.rsquared])
                    except:
                        continue



if __name__ == '__main__':
    pass
    # no_fixed()
    # month_fixed()
    # hour_fixed()
    # driver_fixed()
    # driver_hour_fixed()
    # hour_month_fixed()
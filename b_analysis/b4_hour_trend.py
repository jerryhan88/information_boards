import __init__
from init_project import *
#
import pandas as pd
import seaborn as sns; sns.set_style("whitegrid")
import matplotlib.pyplot as plt
import numpy as np
import csv


def run():
    for yy in ['09', '10']:
        ifpath = opath.join(dpath['analysis'], 'whole-ap-20%s.csv' % yy)
        csv_ofpath = opath.join(dpath['4_hourTrend'], 'hourTrend-ap-20%s.csv' % yy)
        #
        terminals = ['T1', 'T2', 'T3', 'BudgetT']
        labels = ['year', 'month', 'day', 'dow', 'hour', 'Qnum', 'terminal']
        records = []
        processed_date_hour = set()
        with open(ifpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                year, month, day, dow, hour = map(int, [row[hid[cn]] for cn in ['year', 'month', 'day', 'dow', 'hour']])
                k = (year, month, day, hour)
                if k in processed_date_hour:
                    continue
                processed_date_hour.add(k)
                for tn in terminals:
                    Qnum = int(row[hid[tn]])
                    records.append([year, month, day, dow, hour, Qnum, tn])
        df = pd.DataFrame.from_records(records, columns=labels)
        df.to_csv(csv_ofpath, index=False)
        #
        img_ofpath = opath.join(dpath['4_hourTrend'], 'hourTrend-ap-20%s.pdf' % yy)
        _figsize = (8, 6)
        fig = plt.figure(figsize=_figsize)
        fig.add_subplot(111)
        sns.barplot(x="hour", y="Qnum", hue="terminal", data=df)
        plt.yticks(np.arange(0, 200, 20))
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
        #
        for dow in set(df['dow']):
            dow_df = df[(df['dow'] == dow)]
            img_ofpath = opath.join(dpath['4_hourTrend'], 'hourTrend-ap-20%s-%s.pdf' % (yy, DOW[dow]))
            _figsize = (8, 6)
            fig = plt.figure(figsize=_figsize)
            fig.add_subplot(111)
            sns.barplot(x="hour", y="Qnum", hue="terminal", data=dow_df)
            plt.yticks(np.arange(0, 200, 20))
            plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)


# TODO
# add queueing time

if __name__ == '__main__':
    run()

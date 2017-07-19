import __init__
from init_project import *
#
import pandas as pd
import csv


def basicProcess(yy):
    ifpath = opath.join(dpath['ap_QidQNum'], 'ap-QidQNum-20%s.csv' % yy)
    df = pd.read_csv(ifpath)
    df.sort_values(['tPickup'], ascending=[True])
    #
    df['tMaxFirstFreePrevDropoff'] = df.apply(lambda row: row['tFirstFree'] if row['tPrevDropoff'] < row['tFirstFree'] else row['tPrevDropoff'], axis=1)
    df['cycleTime'] = df['tDropOff'] - df['tMaxFirstFreePrevDropoff']
    df['productivity'] = df['fare'] / df['cycleTime']
    #
    df['fare'] = df['fare'] / CENT
    df['cycleTime'] = df['cycleTime'] / MIN1
    df['productivity'] = df['productivity'] * HOUR1 / CENT
    #
    df = df[(df['tPrevDropoff'] < df['tPickUp'])]
    df = df[(df['tFirstFree'] < df['tPickUp'])]
    df = df[(df['cycleTime'] < HOUR2)]
    df = df[(df['productivity'] < TH_PRODUCTIVITY)]
    #
    ofpath = opath.join(dpath['analysis'], 'ap-whole-20%s.csv' % yy)
    df.to_csv(ofpath, index=False)
    #
    groupby_df = df.groupby(['year', 'month', 'day', 'hour']).sum().reset_index()
    new_df = groupby_df[['year', 'month', 'day', 'hour', 'fare', 'cycleTime']]
    new_df['productivity'] = new_df['fare'] / new_df['cycleTime'] * MIN1
    ofpath = opath.join(dpath['analysis'], 'ap-hourProductivity-20%s.csv' % yy)
    new_df.to_csv(ofpath, index=False)



def dropoffAP_dataProcess(yy):
    ifpath = opath.join(dpath['analysis'], 'ap-hourProductivity-20%s.csv' % yy)
    hourProductivity = {}
    with open(ifpath, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        for row in reader:
            year, month, day, hour = map(int, [row[hid[cn]] for cn in ['year', 'month', 'day', 'hour']])
            hourProductivity[year, month, day, hour] = eval(row[hid['productivity']])

    # economic profit!!!
    pass




def pickupAP_dataProcess():
    pass







if __name__ == '__main__':
    # basicProcess('09')
    basicProcess('10')

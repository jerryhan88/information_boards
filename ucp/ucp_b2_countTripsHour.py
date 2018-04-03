import sys, os
import pandas as pd

sorting_order = ['T1', 'T2', 'T3', 'BT', 'XAP']


def run(ifpath, ofpath):
    df = pd.read_csv(ifpath)
    df = df.groupby(['hour', 'origin', 'destination']).sum()['flow'].reset_index()

    df['sortingLabel'] = df.apply(lambda row: row['hour'] * 100 +
                                      sorting_order.index(row['origin']) * 10 +
                                      sorting_order.index(row['destination']), axis=1)
    df = df.sort_values(by=['sortingLabel'], ascending=True)
    df = df.drop(['sortingLabel'], axis=1)
    df.to_csv(ofpath, index=False)




if __name__ == '__main__':
    if len(sys.argv) == 3:
        ifpath, ofpath = [sys.argv[i] for i in range(1, 3)]
    else:
        ifpath = 'tripCount-1704.csv'
        ofpath = 'tripCountHour-1704.csv'

    run(ifpath, ofpath)
import sys, os
import os.path as opath
import pandas as pd


def run(trip_fpath, ofpath):
    df = None
    for fn in os.listdir(trip_fpath):
        if fn.startswith('dayTrip') and fn.endswith('.csv'):
            if df is None:
                df = pd.read_csv(opath.join(trip_fpath, fn))
            else:
                df.append(pd.read_csv(opath.join(trip_fpath, fn)))

    new_df = df.groupby(['year', 'month', 'day', 'hour', 'locPrevDropoff', 'locPickup']).count()['tripType'].reset_index()
    new_df = new_df.rename(columns={'locPrevDropoff': 'origin', 'locPickup': 'destination', 'tripType': 'flow'})
    new_df['origin'][new_df['origin'] == 'BudgetT'] = 'BT'
    new_df['origin'][new_df['origin'] == 'X'] = 'XAP'
    new_df['destination'][new_df['destination'] == 'BudgetT'] = 'BT'
    new_df['destination'][new_df['destination'] == 'X'] = 'XAP'
    new_df.to_csv(ofpath)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        trip_fpath, ofpath = sys.argv[1], sys.argv[2]
    else:
        assert False

    run(trip_fpath, ofpath)
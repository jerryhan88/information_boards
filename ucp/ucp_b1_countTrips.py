import sys, os
import os.path as opath
import pandas as pd


def run(trip_dir, ofpath1, ofpath2):
    if not opath.exists(ofpath1):
        df = None
        for fn in sorted([fn for fn in os.listdir(trip_dir) if fn.startswith('dayTrip') and fn.endswith('.csv')]):
            trip_fpath = opath.join(trip_dir, fn)
            if df is None:
                df = pd.read_csv(trip_fpath)
            else:
                df = df.append(pd.read_csv(trip_fpath))
            print(len(df), fn)

        new_df = df.groupby(['year', 'month', 'day', 'hour', 'locPrevDropoff', 'locPickup']).count()['tripType'].reset_index()
        new_df = new_df.rename(columns={'locPrevDropoff': 'origin', 'locPickup': 'destination', 'tripType': 'flow'})
        new_df['origin'][new_df['origin'] == 'BudgetT'] = 'BT'
        new_df['origin'][new_df['origin'] == 'X'] = 'XAP'
        new_df['destination'][new_df['destination'] == 'BudgetT'] = 'BT'
        new_df['destination'][new_df['destination'] == 'X'] = 'XAP'
        new_df.to_csv(ofpath1, index=False)
        df = new_df
    else:
        df = pd.read_csv(ofpath1)
    new_df = df.groupby(['origin', 'destination']).sum()['flow'].reset_index()
    new_df.to_csv(ofpath2, index=False)


if __name__ == '__main__':
    if len(sys.argv) == 4:
        trip_fpath, ofpath1, ofpath1 = [sys.argv[i] for i in range(1, 4)]
    else:
        assert False

    run(trip_fpath, ofpath1, ofpath1)
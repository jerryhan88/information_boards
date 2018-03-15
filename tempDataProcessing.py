from init_project import *

import pandas as pd

df = pd.read_csv(opath.join(dpath['_data'], 'wholeAP-2010.csv'))

df.columns

new_df = df.groupby(['year', 'month', 'day', 'hour', 'locPrevDropoff', 'locPickup']).count()['cycleTime'].reset_index()
new_df = new_df.rename(columns={'locPrevDropoff': 'origin', 'locPickup': 'destination', 'cycleTime': 'flow'})
new_df['origin'][new_df['origin'] == 'BudgetT'] = 'BT'
new_df['origin'][new_df['origin'] == 'X'] = 'XAP'
new_df['destination'][new_df['destination'] == 'BudgetT'] = 'BT'
new_df['destination'][new_df['destination'] == 'X'] = 'XAP'

new_df.to_csv('wholeAP-Flow-2010.csv')

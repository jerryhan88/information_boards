import os.path as opath
import pandas as pd
from datetime import datetime, timedelta
#
from __path_organizer import aggr_dpath, h2data_dpath
from __common import TERMINALS1, TERMINALS2

AM2, AM6 = 2, 6
TARGET_HOURS1 = list(range(AM6, 24))
TARGET_HOURS2 = list(range(AM2))

def arrange_datasets():
    yyyys = ['2009', '2010']
    for yyyy in yyyys:
        yyyy = '2009'
        terminals = TERMINALS1 if yyyy != '2018' else TERMINALS2
        ifpath = opath.join(aggr_dpath, 'apTrip-%s.csv' % yyyy)
        df = pd.read_csv(ifpath)
        
        
        df['dt_enter'] = df.apply(lambda row: datetime.fromtimestamp(row['time_enter_airport']), axis=1)
        df['dt_exit'] = df.apply(lambda row: datetime.fromtimestamp(row['time_exit_airport']), axis=1)
        earliest_dt = df['dt_enter'].min()
        
        cdt = datetime(earliest_dt.year, earliest_dt.month, earliest_dt.day)
        cdf = df[(df['month'] == cdt.month) & (df['day'] == cdt.day) & (df['hour'].isin(TARGET_HOURS1))]
        
        ndt = cur_dt + timedelta(days=1)
        ndf = df[(df['month'] == ndt.month) & (df['day'] == ndt.day) & (df['hour'].isin(TARGET_HOURS2))]
        
        tdf = cdf.append(ndf)
        
        tdf.head()
        
        inter_begin += timedelta(hours=1)
        inter_end += timedelta(hours=1)
        
        inter_begin = datetime(cur_dt.year, cur_dt.month, cur_dt.day, AM6) + timedelta(minutes=0)
        inter_end = datetime(cur_dt.year, cur_dt.month, cur_dt.day, AM6) + timedelta(hours=1)
        tn_numTaxis = []
        tn_df = {tn: tdf[(tdf['start_loc'] == tn)] for tn in terminals}
        for tn in terminals:
            ter_df = tn_df[tn]
            qNum = len(ter_df[(ter_df['dt_enter'] <= inter_begin) & (ter_df['dt_exit'] >= inter_end)])
            tn_numTaxis.append(qNum)
        
        
        
        ofpath = opath.join(h2data_dpath, 'apQNum-%s.csv' % yyyy)
        with open(ofpath, 'w') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_header = ['year', 'month', 'day', 'hour']
            new_header += terminals
            writer.writerow(new_header)
        
        
        
        
        ymdh_tn_
        with open(ifpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            header = reader.next()        

        
        

    ifpath = opath.join(dpath['_data'], 'wholeAP-20%s.csv' % yy)
    ofpath = opath.join(dpath['_data'], 'wholeAP-QNum-20%s.csv' % yy)
    terminals = ['T1', 'T2', 'T3', 'BudgetT']
    labels = ['year', 'month', 'day', 'dow', 'hour', 'terminal', 'QNum']
    records = []
    processed_date_hour = set()
    with open(ifpath, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        header = reader.next()
        hid = {h: i for i, h in enumerate(header)}
        for row in reader:
            year, month, day, dow, hour = map(int, [row[hid[cn]] for cn in ['year', 'month', 'day', 'dow', 'hour']])
            k = (year, month, day, hour)
            if k in processed_date_hour:
                continue
            processed_date_hour.add(k)
            for tn in terminals:
                QNum = int(row[hid[tn]])
                records.append([year, month, day, dow, hour, tn, QNum])
    df = pd.DataFrame.from_records(records, columns=labels)
    df.to_csv(ofpath, index=False)


if __name__ == '__main__':
    pass
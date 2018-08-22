import os.path as opath
import pandas as pd


def arrange_datasets():
    yyyys = ['2009', '2010']
    for yyyy in yyyys:
        yyyy = '2009'
        df = pd.read_csv(opath.join(aggr_dpath, 'apTrip-%s.csv' % yyyy))

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
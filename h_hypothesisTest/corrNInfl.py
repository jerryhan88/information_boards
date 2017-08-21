import __init__
from init_project import *
#
import pandas as pd
import seaborn as sns; sns.set_style("whitegrid")
import matplotlib.pyplot as plt
import statsmodels.api as sm

MIN_NTrips = 11 * 10

BUBBLE_SIZE = 2

def run():
    csv_ofpath = opath.join(dpath['hypCorrNInfl'], 'driver2010-measures.csv')
    corr_img_ofpath = opath.join(dpath['hypCorrNInfl'], 'correlation.pdf')
    corr_csv_ofpath = opath.join(dpath['hypCorrNInfl'], 'correlation.csv')
    pQ2dQ_ofpath = opath.join(dpath['hypCorrNInfl'], 'regression-pQ2dQ.txt')
    dQ2pQ_ofpath = opath.join(dpath['hypCorrNInfl'], 'regression-dQ2pQ.txt')
    #
    if not opath.exists(csv_ofpath):
        pickupAP_df = pd.read_csv(opath.join(dpath['_data'], 'pickupAP-2010.csv'))
        dropoffAP_df = pd.read_csv(opath.join(dpath['_data'], 'dropoffAP-2010.csv'))
        #
        pNTrip_df = pickupAP_df.groupby(['did']).count()['year'].to_frame('NTrip').reset_index()
        pNTrip_df = pNTrip_df[(pNTrip_df['NTrip'] > MIN_NTrips)]
        dNTrip_df = dropoffAP_df.groupby(['did']).count()['year'].to_frame('NTrip').reset_index()
        dNTrip_df = dNTrip_df[(dNTrip_df['NTrip'] > MIN_NTrips)]
        pickupAP_drivers, dropoffAP_drivers = map(set, [pNTrip_df['did'], dNTrip_df['did']])
        bc_drivers = pickupAP_drivers.intersection(dropoffAP_drivers)
        pickupAP_df = pickupAP_df.drop(pickupAP_df[~(pickupAP_df['did'].isin(bc_drivers))].index)
        dropoffAP_df = dropoffAP_df.drop(dropoffAP_df[~(dropoffAP_df['did'].isin(bc_drivers))].index)
        #
        pd_df = pickupAP_df.groupby(['did']).mean()[['QTime', 'QScore']].reset_index()
        dd_df = dropoffAP_df.groupby(['did']).mean()[['ecoProfit', 'QScore']].reset_index()
        labels = ['did', 'pQScore', 'QTime', 'dQScore', 'ecoProfit']
        records = []
        for did in bc_drivers:
            _, QTime, pickupQScore = pd_df.loc[(pd_df['did'] == did)].values.tolist()[0]
            _, ecoProfit, dropoffQScore = dd_df.loc[(dd_df['did'] == did)].values.tolist()[0]
            records.append([did, pickupQScore, QTime, dropoffQScore, ecoProfit])
        df = pd.DataFrame.from_records(records, columns=labels)
        df.to_csv(csv_ofpath, index=False)
    else:
        df = pd.read_csv(csv_ofpath)
    df.drop('did', axis=1, inplace=True)
    #
    fig = plt.figure(figsize=FIGSIZE)
    fig.add_subplot(111)
    g = sns.pairplot(df, plot_kws={"s": BUBBLE_SIZE})
    g.map(plt.scatter, s=BUBBLE_SIZE)
    plt.savefig(corr_img_ofpath, bbox_inches='tight', pad_inches=0)
    df.corr().to_csv(corr_csv_ofpath)
    #
    y = df['dQScore']
    X = df[['pQScore']]
    X = sm.add_constant(X)
    res = sm.OLS(y, X, missing='drop').fit()
    with open(pQ2dQ_ofpath, 'w') as f:
        f.write(res.summary().as_text())
    #
    y = df['pQScore']
    X = df[['dQScore']]
    X = sm.add_constant(X)
    res = sm.OLS(y, X, missing='drop').fit()
    with open(dQ2pQ_ofpath, 'w') as f:
        f.write(res.summary().as_text())
    
    

if __name__ == '__main__':
    run()
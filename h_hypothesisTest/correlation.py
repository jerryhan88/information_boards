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
    csv_ofpath = opath.join(dpath['hypCorr'], 'driver2010-measures.csv')
    corr_img_ofpath = opath.join(dpath['hypCorr'], 'correlation.pdf')
    corr_csv_ofpath = opath.join(dpath['hypCorr'], 'correlation.csv')
    #
    if not opath.exists(csv_ofpath):
        wholeAP_df = pd.read_csv(opath.join(dpath['_data'], 'wholeAP-2010.csv'))
        pickupAP_df = pd.read_csv(opath.join(dpath['_data'], 'pickupAP-2010.csv'))
        dropoffAP_df = pd.read_csv(opath.join(dpath['_data'], 'dropoffAP-2010.csv'))
        dropoffXAP_df = pd.read_csv(opath.join(dpath['_data'], 'dropoffXAP-2010.csv'))
        drivers = []
        for df in [pickupAP_df, dropoffAP_df, dropoffXAP_df]:
            df_NTrip = df.groupby(['did']).count()['year'].to_frame('NTrip').reset_index()
            df_NTrip = df_NTrip[(df_NTrip['NTrip'] > MIN_NTrips)]
            drivers.append(set(df_NTrip['did']))
        subDrivers = reduce(lambda x ,y: x.intersection(y), drivers)
        wholeAP_df = wholeAP_df.drop(wholeAP_df[~(wholeAP_df['did'].isin(subDrivers))].index)
        pickupAP_df = pickupAP_df.drop(pickupAP_df[~(pickupAP_df['did'].isin(subDrivers))].index)
        dropoffAP_df = dropoffAP_df.drop(dropoffAP_df[~(dropoffAP_df['did'].isin(subDrivers))].index)
        dropoffXAP_df = dropoffXAP_df.drop(dropoffXAP_df[~(dropoffXAP_df['did'].isin(subDrivers))].index)
        #
        did_prod = wholeAP_df.groupby(['did']).mean()[['productivity']].reset_index()
        did_QT_pDS = pickupAP_df.groupby(['did']).mean()[['QTime', 'DScore']].reset_index()
        did_EP_dDS = dropoffAP_df.groupby(['did']).mean()[['ecoProfit', 'DScore']].reset_index()
        did_xDS = dropoffXAP_df.groupby(['did']).mean()[['DScore']].reset_index()
        #
        labels = ['did', 'productivity', 'QTime', 'ecoProfit', 'pDScore', 'dDScore', 'xDScore']
        records = []
        for did in subDrivers:
            _, productivity = did_prod.loc[(did_prod['did'] == did)].values.tolist()[0]
            _, QTime, pDScore = did_QT_pDS.loc[(did_prod['did'] == did)].values.tolist()[0]
            _, ecoProfit, dDScore = did_EP_dDS.loc[(did_EP_dDS['did'] == did)].values.tolist()[0]
            _, xDScore = did_xDS.loc[(did_xDS['did'] == did)].values.tolist()[0]
            records.append([did, productivity, QTime, ecoProfit, pDScore, dDScore, xDScore])
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
    

if __name__ == '__main__':
    run()
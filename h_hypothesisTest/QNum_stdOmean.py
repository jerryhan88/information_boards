import __init__
from init_project import *
#
import pandas as pd
import seaborn as sns; sns.set_style("whitegrid")
import matplotlib.pyplot as plt


def run_QNum_stdOmean():
    def process_QNum_stdOmean(_df, img_ofpath):
        m_hdf = _df.groupby(['year', 'hour']).mean()['QNum'].to_frame('meanQNum').reset_index()
        sd_hdf = _df.groupby(['year', 'hour']).std()['QNum'].to_frame('stdQNum').reset_index()
        yearHour_QNumM = {(year, hour): QNumM for year, hour, QNumM in m_hdf.values}
        yearHour_QNumSD = {(year, hour): QNumSD for year, hour, QNumSD in sd_hdf.values}
        hours = sorted(list(set(m_hdf['hour'])))
        fig = plt.figure(figsize=FIGSIZE)
        ax = fig.add_subplot(111)
        ax.set_xlabel('hour')
        # ax.set_ylabel('QNum SD / M')
        for i, year in enumerate([2009, 2010]):
            plt.plot(range(len(hours)), [yearHour_QNumSD[year, hour] / float(yearHour_QNumM[year, hour]) for hour in hours],
                     color=clists[i], marker=mlists[i])
        plt.legend(['2009', '2010'], ncol=1, loc='upper left')
        plt.xticks(range(len(hours)), hours)
        plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    df = pd.read_csv(opath.join(dpath['_data'], 'wholeAP-QNum-2009.csv'))
    df = df.append(pd.read_csv(opath.join(dpath['_data'], 'wholeAP-QNum-2010.csv')))
    #
    img_ofpath = opath.join(dpath['hQNumSTDoM'], 'hQNumSTDoM.pdf')
    process_QNum_stdOmean(df, img_ofpath)


if __name__ == '__main__':
    run_QNum_stdOmean()

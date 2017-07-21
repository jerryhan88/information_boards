import b_analysis
from init_project import *
#
import pandas as pd
import seaborn as sns; sns.set(style="ticks", color_codes=True)
import matplotlib.pyplot as plt


def run(yy):
    ifpath = opath.join(dpath['analysis'], 'decision-ap-20%s.csv' % yy)
    ofpath = opath.join(dpath['3_correlation'], 'correlation-ap-20%s.png' % yy)
    #
    df = pd.read_csv(ifpath)
    df = df[['fare', 'duration', 'qrTime', 'productivity', 'oppoCost', 'ecoProfit']]
    #
    _figsize = (8, 6)
    fig = plt.figure(figsize=_figsize)
    fig.add_subplot(111)
    g = sns.pairplot(df)
    g.map(plt.scatter, s=0.001)
    plt.savefig(ofpath, bbox_inches='tight', pad_inches=0)


if __name__ == '__main__':
    run('09')
    # run('10')

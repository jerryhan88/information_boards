import __init__
from init_project import *
#
import seaborn as sns; sns.set_style("whitegrid")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv


def run_SCost():
    instances = []
    year_cost_num = {}
    bin_range = list(range(0, 130, 10))
    for yyyy in [2009, 2010]:
        df = pd.read_csv(opath.join(dpath['_data'], 'dropoffXAP-%d.csv' % yyyy))
        count, _ = np.histogram(df[(df['GA'] == 0)]['sunkCost'], bins=bin_range)
        for i in range(len(bin_range) - 1):
            sunkCost, num = bin_range[i] + 10, count[i]
            instances.append({'Year': yyyy, 'sunkCost': sunkCost, 'num': num})
            year_cost_num[yyyy, sunkCost] = num
    df = pd.DataFrame(instances)
    img_ofpath = opath.join(dpath['hypSCost'], 'sunkCostHist.pdf')
    fig = plt.figure(figsize=FIGSIZE)
    fig.add_subplot(111)
    ax = fig.add_subplot(111)
    sns.barplot(x="sunkCost", y="num", hue="Year", hue_order=[2009, 2010], data=df)
    ax.set_xlabel('Sunk cost')
    ax.set_ylabel('')
    # plt.ylim((0, 100))
    # plt.yticks(np.arange(0, 100, 20))
    plt.savefig(img_ofpath, bbox_inches='tight', pad_inches=0)
    #
    csv_ofpath = opath.join(dpath['hypSCost'], 'sunkCostHist.csv')
    bin_range = list(set(df['sunkCost'])); bin_range.sort()
    with open(csv_ofpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        new_headers = ['sunkCost', 'Y2009', 'Y2010', 'Diff.', '%%']
        writer.writerow(new_headers)
        for v in bin_range:
            num2009, num2010 = year_cost_num[2009, v], year_cost_num[2010, v]
            diff = num2010 - num2009
            writer.writerow([v, num2009, num2010, diff, (diff / float(num2009)) * 100])


if __name__ == '__main__':
    run_SCost()
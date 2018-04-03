import os.path as opath
import os


import numpy as np
import matplotlib.pyplot as plt
from xlrd import open_workbook


terminals = ['T1', 'T2', 'T3', 'BT', 'XAP']
terminalsWtotal = terminals + ['Total']
_figsize = (10, 4)


def draw_chart(ifpath, ofpath):
    book = open_workbook(ifpath)
    sh = book.sheet_by_name('Percentage')

    terminal_percentage = []
    for i in range(3, 9):
        terminal_percentage.append([sh.cell(i, j).value for j in range(3, 8)])
    datasets = [np.array(v) * 100 for v in zip(*terminal_percentage)]

    plt.figure(figsize=_figsize)
    ind = np.arange(len(terminalsWtotal))
    width = 0.35

    bottomVals = None
    chart_info = []
    for data in datasets:
        if bottomVals is None:
            c = plt.bar(ind, data, width)
            bottomVals = data
        else:
            c = plt.bar(ind, data, width, bottom=bottomVals)
            bottomVals += data
        chart_info.append(c[0])
    plt.ylabel('Percentage')
    plt.xlabel('Origin')
    plt.xticks(ind, terminalsWtotal)
    plt.yticks(np.arange(0, 120, 20))
    plt.ylim((0, 100))
    plt.legend(chart_info[::-1], terminals[::-1])
    plt.savefig(ofpath, bbox_inches='tight', pad_inches=0)
    plt.close()


def run():
    for fn in os.listdir('AirportFlow'):
        if not fn.endswith('.xlsx'):
            continue
        prefix = fn[:-len('.xlsx')]
        ifpath = opath.join('AirportFlow', fn)
        ofpath = opath.join('AirportFlow', 'barChart_%s.pdf' % prefix)
        draw_chart(ifpath, ofpath)



if __name__ == '__main__':
    run()
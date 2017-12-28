import matplotlib.pyplot as plt
import os
import numpy as np
from io import BytesIO
# return locs, labels where locs is an array of tick locations and
# labels is an array of tick labels.


def plotbar(names, yvalues, fname='', suffix='png'):
    ind = np.arange(len(yvalues))  # the x locations for the groups
    width = 0.35  # the width of the bars: can also be len(x) sequence
    plt.bar(ind, yvalues, width, color='#d62728')
    plt.ylabel('number of each category')
    plt.title('categories')

    #plt.xticks(ind, names, rotation=45, fontsize='small')

    ## test part
    ind = 2 * (ind)
    names = names[0: -2]
    plt.xticks(ind, names, rotation=45)

    plt.yticks(np.arange(0, 81, 100))
    plt.yscale('log')
    plt.ylim(ymin=100)
    if fname != '':
        plt.savefig(fname)
    plt.show()

def plotbar_size(names, yvalues, category, xmin, xmax, fname='', suffix='eps'):
    ind = np.arange(len(yvalues))  # the x locations for the groups
    gap = int((xmax - xmin) / len(yvalues))
    width = 0.6  # the width of the bars: can also be len(x) sequence
    plt.bar(ind, yvalues, width, color='#d62728')
    plt.ylabel('numbers')
    plt.xlabel('size distribution of ' + category + '(pixel)')
#    plt.title('size distribution of plane ()')

    ind2 = gap * np.arange(len(names))
    plt.xticks(ind2, names, fontsize='small')
    #plt.yticks(np.arange(0, 1000, 10))
    plt.yscale('log')
    plt.ylim(ymin=10)
    plt.xlim(xmin=xmin, xmax=xmax)
    if fname != '':
        plt.savefig(fname)
    plt.show()

def testplotbar():
    names = ('G1', 'G2', 'G3', 'G4', 'G5')
    yvalues = (10000, 30000, 300, 1000, 3000)
    plotbar(names, yvalues)

def plotNumberDistribution():
    pass
if __name__ == '__main__':
    testplotbar()
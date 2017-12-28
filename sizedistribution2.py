from utils import GetFileFromThisRootDir
from parse_geotiff import parge_geotiff
import numpy as np
import os
import utils as util
import codecs
from plot import plotbar_size
import pickle
import matplotlib.pyplot as plt

class SizeDistribution(object):
    def __init__(self,
                 basepath):
        self.classs_physic = {'ground-track-field': [], 'small-vehicle': [], 'large-vehicle': [], 'harbor': [], 'plane': [], 'ship': [],
                      'basketball-court': [], 'swimming-pool': [], 'helicopter': [], 'bridge': [], 'tennis-court': [],
                      'baseball-diamond': [], 'storage-tank': [], 'soccer-ball-field': [], 'turntable': [],
                      }
        self.classs_pixel = {'ground-track-field': [], 'small-vehicle': [], 'large-vehicle': [], 'harbor': [], 'plane': [], 'ship': [],
                      'basketball-court': [], 'swimming-pool': [], 'helicopter': [], 'bridge': [], 'tennis-court': [],
                      'baseball-diamond': [], 'storage-tank': [], 'soccer-ball-field': [], 'turntable': [],
                      }
        self.basepath = basepath
        self.respath = os.path.join(self.basepath, 'resolution')
        self.imgpath = os.path.join(self.basepath, 'images')
        self.labelpath = os.path.join(self.basepath, 'wordlabel')
        self.barnum = 28
        self.xname_num = 8
        self.picklepath = os.path.join(self.basepath, 'pickle')
        if not os.path.exists(os.path.join(self.picklepath, 'physic.pickle')):
            self.sizeAnalysis('pixel')
        else:
            with open(os.path.join(self.picklepath, 'physic.pickle'), 'rb') as f:
                pickle.dump(self.classs_physic, f)
        self.sizeAnalysis('physic')
    def getresolution(self, name):
        resname = os.path.join(self.respath, name + '.txt')
        with open(resname, 'r') as f:
            line = f.readline()
            resolution = line.strip()
        return resolution

    def plotbar_size(self, names, yvalues, category, xmin, xmax, fname='', suffix='.eps', type='physic'):
        ind = np.arange(len(yvalues))  # the x locations for the groups
        print 'xmin:', xmin
        print 'xmax:', xmax
        gap = int((float(xmax) - float(xmin)) / self.xname_num)
        width = 0.6  # the width of the bars: can also be len(x) sequence
        plt.bar(ind, yvalues, width, color='#d62728')
        plt.ylabel('numbers')
        plt.xlabel('size distribution of ' + category + type)
        #    plt.title('size distribution of plane ()')

        ind2 = self.barnum/self.xname_num * np.arange(len(names))
        plt.xticks(ind2, names, fontsize='small')
        # plt.yticks(np.arange(0, 1000, 10))
        plt.yscale('log')
        plt.ylim(ymin=10)
        plt.xlim(xmin=0, xmax=self.barnum)
        if fname != '':
             plt.savefig(fname)
        plt.show()

    def sizeAnalysis(self, type='physic'):
        filelist = GetFileFromThisRootDir(self.imgpath)
        for fullname in filelist:
            if 'Thumbs' in fullname:
                continue
            name = util.mybasename(fullname)

            resolution = self.getresolution(name)
            #print 'resolution:', resolution
            if (resolution == ''):
                continue
            resolution = float(resolution)
            labelname = os.path.join(self.labelpath, name + '.txt')
            objects = util.parse_bod_poly(labelname)
            for obj in objects:
                assert obj['name'] in self.classs_pixel, 'the name is not in 15 classes'
                wordname = obj['name']
                if type == 'physic':
                    lenth = resolution * obj['long-axis']
                    #if (wordname == 'small-vehicle'):
                       # assert lenth <= 15, 'the small-vehicle should shorter than 15, ' + 'wrong imgname is ' + fullname
                    self.classs_pysic[wordname].append(lenth)
                elif type == 'pixel':
                    lenth = obj['long-axis']
                    self.classs_pixel[wordname].append(lenth)
                ## 2 is the gap between
    def generateplotX_Y(self, class_name, flag='physic'):
        if (flag == 'physic'):
            lengths = self.classs_pysic[class_name]
        elif (flag == 'pixel'):
            lengths = self.classs_pixel[class_name]
        len_min = min(lengths)
        len_max = max(lengths)
        print 'type len_min:', type(len_min)
        print 'len_min:', len_min
        print 'len_max:', len_max
        name_gap = (len_max - len_min) / self.xname_num
        X_names = name_gap * np.arange(self.xname_num) + len_min
        X_names = list(map(str, X_names))
        Y_gap = (len_max - len_min) / self.barnum
        yvalues = np.arange(self.barnum)
        for length in lengths:
            pos = int((length - len_min) / Y_gap)
            pos = min(pos, 27)
            yvalues[pos] = yvalues[pos] +1
        return X_names, yvalues, len_min, len_max

    def plotpixel(self):
        #self.sizeAnalysis('pixel')
        for class_name in self.classsizes:
            X_names, yvalues, xmin, xmax = self.generateplotX_Y(class_name, 'pixel')
            self.plotbar_size(X_names, yvalues, class_name, xmin, xmax, 'pixel')

    def plotphysic(self):
        #self.sizeAnalysis('physic')
        for class_name in self.classsizes:
            X_names, yvalues, xmin, xmax = self.generateplotX_Y(class_name, 'physic')
            self.plotbar_size(X_names, yvalues, class_name, xmin, xmax, 'physic')
if __name__ == '__main__':
    sizeplot = SizeDistribution(r'E:\bod-dataset')
    X_names, yvalues, len_min, len_max = sizeplot.generateplotX_Y('small-vehicle')
    print 'len_min:', len_min
    print 'len_max:', len_max

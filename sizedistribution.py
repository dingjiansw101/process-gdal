from utils import GetFileFromThisRootDir
from parse_geotiff import parge_geotiff
import numpy as np
import os
import utils as util
import codecs
from plot import plotbar_size
import pickle


## prepare for release 1.0 version
datamap_19 = {'0A': 'plane', '0B':'plane', '0C': 'plane',  '1': 'baseball diamond', '2': 'bridge', '3': 'ground track field', '4A': 'vehicle', '4B': 'vehicle',
           '4C': 'vehicle', '5A': 'ship', '5B':'ship', '6': 'tennis court', '7': 'basketball court',
           '8': 'storage tank', '9': 'soccer ball field', '10': 'turntable',
           '11': 'harbor', '12': 'electric pole', '13': 'parking lot', '14': 'swimming pool', '15': 'lake',
           '16': 'helicopter', '17': 'airport', '18A': 'viaduct', '18B': 'overpass', '18C': 'overpass', '18D': 'overpass',
              '18E': 'overpass', '18F': 'overpass', '18G': 'overpass', '18H': 'overpass', '18I': 'overpass', '18J': 'overpass',
              '18K': 'overpass', '18L': 'overpass', '18M': 'overpass', '18N': 'overpass'}

classname_19 = ['0A', '0B', '0C', '1', '2', '3', '4A', '4B', '4C', '5A', '5B', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18A', '18B', '18C', '18D', '18E'
    , '18F', '18G', '18H', '18I', '18J', '18K', '18L', '18M', '18N']

wordname_19 = ['plane', 'baseball diamond', 'bridge', 'ground track field', 'vehicle', 'ship', 'tennis court',
               'basketball court', 'storage tank', 'soccer ball field', 'turntable', 'harbor', 'electric pole',
               'parking lot', 'swimming pool', 'lake', 'helicopter', 'airport', 'viaduct', 'overpass']
# clsdict_19 = {'0A': 0, '0B': 0, '0C': 0, '1': 0, '2': 0, '3': 0, '4A': 0, '4B': 0, '4C': 0, '5A': 0, '5B': 0, '6': 0,
#            '7': 0, '8': 0, '9': 0, '10': 0
#     , '11': 0, '12': 0, '13': 0, '14': 0, '15': 0, '16': 0, '17': 0, '18A': 0}

classsizes = { 'ground track field':[], 'vehicle':[], 'parking lot':0, 'harbor':0, 'plane':0, 'ship':0, 'basketball court':0,
              'swimming pool':[], 'lake':0, 'helicopter':0, 'electric pole':0, 'viaduct':0, 'bridge':0, 'tennis court':0,
              'baseball diamond':[], 'storage tank':0, 'airport':0, 'soccer ball field':0, 'turntable':0, 'overpass':0 }

classzies_15 = {'ground'}

## np.array() for each category will become bars, the gap between two bar is 2m.
gap = np.int(2)
maxn = 150
def init():
    for keys in classsizes:
        classsizes[keys] = np.zeros(maxn)
init()
coordinate_x = [str(20*x) for x in range(15)]

def sizeAnalysis(path, classname_part, type='physic'):
    geopath = os.path.join(path, 'images')
    labelpath = os.path.join(path, 'labelTxt')
    filelist = GetFileFromThisRootDir(geopath)
    for fullname in filelist:
        resolution = parge_geotiff(fullname)
        name = util.mybasename(fullname)
        labelname = os.path.join(labelpath, name + '.txt')
        objects = util.parse_bod_poly(labelname)
        for obj in objects:
            if obj['name'] not in classname_19:
                continue
            if datamap_19[obj['name']] not in classname_part:
                continue
            wordname = datamap_19[obj['name']]
            if type == 'physic':
                lenth = resolution * obj['long-axis']
            elif type == 'pixel':
                lenth = obj['long-axis']
            ## 2 is the gap between
            index = int(lenth/gap)
            #print 'wordname:', wordname
            if (index < maxn):
                classsizes[wordname][index] = classsizes[wordname][index] + 1

def testsizeAnalysis():
    stasticpath = r'E:\GoogleEarth\up-9-25-data\secondjpg\stastics\pixel'
    basepath = r'E:\GoogleEarth\up-9-25-data\secondjpg'
    testpath = os.path.join(basepath, 'test')
    trainpath = os.path.join(basepath, 'train')
    classname_part = ['plane', 'vehicle', 'storage tank', 'helicopter', 'basketball court',
                      'tennis court', 'turntable', 'baseball diamond', 'soccer ball field', 'ship']
    sizeAnalysis(testpath, classname_part, 'pixel')
    sizeAnalysis(trainpath, classname_part, 'pixel')

    for name in classname_part:
        print 'name:', name
        print 'classizes:', classsizes[name]
        outname = os.path.join(stasticpath, name + '.pickle')
        with open(outname, 'wb') as f:
            pickle.dump(classsizes[name], f, pickle.HIGHEST_PROTOCOL)
        saveimgpath = os.path.join(stasticpath, name + '.png')
        plotbar_size(coordinate_x, classsizes[name], name, saveimgpath)

if __name__ == '__main__':
    testsizeAnalysis()


from utils import GetFileFromThisRootDir
import numpy as np
import os
import utils as util
import codecs
from plot import plotbar_size
import pickle
import matplotlib.pyplot as plt
import shapely.geometry as shgeo
from osgeo import gdal
from osgeo import ogr
def traverse_geotif(namelist):
    ## imgboxs are list of shgeo.Polygon
    basepath = r'E:\GoogleEarth\up-9-25-data\secondjpg'
    geotifs = util.GetFileFromThisRootDir(basepath, '.tif')

    geotifnames = [x for x in geotifs if util.mybasename(x) in namelist]
    imgboxs = []
    for tifname in geotifnames:
        #print 'tifname:', tifname
        imgpoly = parge_geotiff(tifname)
        name = util.mybasename(tifname)
        imgboxs.append([name, imgpoly])
    return imgboxs
def parge_geotiff(filename):
    dataset = gdal.Open(filename, gdal.GA_ReadOnly)
    print 'fullname:', filename
    #print("Driver: {}/{}".format(dataset.GetDriver().ShortName,
    #                             dataset.GetDriver().LongName))


    # print("Size is {} x {} x {}".format(dataset.RasterXSize,
    #                                    dataset.RasterYSize,
    #                                    dataset.RasterCount))
    # print("Projection is {}".format(dataset.GetProjection()))
    geotransform = dataset.GetGeoTransform()
    if geotransform:
        pass
        # print("Origin = ({}, {})".format(geotransform[0], geotransform[3]))
        # print("Pixel Size = ({}, {})".format(geotransform[1], geotransform[5]))
    geo_xmin, geo_ymin = (geotransform[0], geotransform[3])
    geo_xmax = geotransform[0] + geotransform[1] * dataset.RasterXSize
    geo_ymax = geotransform[3] + geotransform[5] * dataset.RasterYSize
    #print geo_xmin, geo_ymin, geo_xmax, geo_ymax
    poly = [(geo_xmin, geo_ymin),
             (geo_xmax, geo_ymin),
             (geo_xmax, geo_ymax),
             (geo_xmin, geo_ymax)]
    #print poly
    imgpoly = shgeo.Polygon(poly)
    return imgpoly

def calc_iou(poly1, poly2):
    inter_poly = poly1.intersection(poly2)
    inter_area = inter_poly.area
    union_poly = poly1.union(poly2)
    union_area = union_poly.area
    #poly1_area = poly1.area
    iou = inter_area / union_area
    return iou

def matcher(imgboxs):
    match_thresh = 0.2
    match_pair = []
    for i in range(len(imgboxs)):
        for j in range(i, len(imgboxs)):
            iou = calc_iou(imgboxs[i][1], imgboxs[j][1])
            if (iou > match_thresh) and (imgboxs[i][0] != imgboxs[j][0]):
                single_matched_pair = (imgboxs[i][0], imgboxs[j][0])
                print 'single_matched_pair: ', single_matched_pair
                match_pair.append(single_matched_pair)
    return match_pair
def test():
    filelist = util.GetFileFromThisRootDir(r'E:\bod-dataset\images')
    namelist = [util.mybasename(x) for x in filelist]
    imgboxs = traverse_geotif(namelist)
    mathes = matcher(imgboxs)
    savepath = r'E:\bod-dataset\pickle\duplicate.pkl'
    with open(savepath, 'wb') as f:
        pickle.dump(mathes, f)
    for item in mathes:
        print item
if __name__ == '__main__':
    test()
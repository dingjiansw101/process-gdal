from osgeo import gdal
from osgeo import ogr
import numpy as np
import cv2
import os
import codecs

def GetFileFromThisRootDir(dir,ext = None):
  allfiles = []
  needExtFilter = (ext != None)
  for root,dirs,files in os.walk(dir):
    for filespath in files:
      filepath = os.path.join(root, filespath)
      extension = os.path.splitext(filepath)[1][1:]
      if needExtFilter and extension in ext:
        allfiles.append(filepath)
      elif not needExtFilter:
        allfiles.append(filepath)
  return allfiles



def parge_geotiff(filename):
    dataset = gdal.Open(filename, gdal.GA_ReadOnly)
    #print 'fullname:', filename
    #print("Driver: {}/{}".format(dataset.GetDriver().ShortName,
    #                             dataset.GetDriver().LongName))
    print("Size is {} x {} x {}".format(dataset.RasterXSize,
                                       dataset.RasterYSize,
                                       dataset.RasterCount))
    forwatch = dataset.GetProjection()
    print("Projection is {}".format(dataset.GetProjection()))
    geotransform = dataset.GetGeoTransform()
    if geotransform:
        print("Origin = ({}, {})".format(geotransform[0], geotransform[3]))
        print("Pixel Size = ({}, {})".format(geotransform[1], geotransform[5]))
    resolution = abs(geotransform[1])
    origin = (geotransform[0], geotransform[3])
    return resolution, origin, dataset.RasterXSize, dataset.RasterYSize

def fromtifgetextent(filename):
    dataset = gdal.Open(filename, gdal.GA_ReadOnly)
    width, height = dataset.RasterXSize, dataset.RasterYSize
    geotransform = dataset.GetGeoTransform()
    xmin, ymin = geotransform[0], geotransform[3]
    xmax = xmin + width * geotransform[1]
    ymax = ymin + height * geotransform[5]
    extent = (xmin, ymin, xmax, ymax)
    return extent

if __name__ == '__main__':
    # basepath = r'E:\GoogleEarth\up-9-25-data\SecondQuality\leiyaxian\all'
    # geotiffpath = os.path.join(basepath, 'images')
    # filelist = GetFileFromThisRootDir(geotiffpath)
    # resolutionpath = os.path.join(basepath, 'resolution')
    # for fullname in filelist:
    #     resolution = parge_geotiff(fullname)
    #     outname = os.path.join(resolutionpath, os.path.basename(os.path.splitext(fullname)[0]) + '_res' + '.txt')
    #     f_out = codecs.open(outname, 'w', 'utf_16')
    #     f_out.write(str(resolution) + '\n')
    #filename = r'G:\LocaSpaceViewer\LocaSpaceViewer\download\TaskIMG12150910\TaskIMG12150910.ltsk'
    filename = r'/home/dingjian/Pictures/airport2/Export00-00-09.tif'
    parge_geotiff(filename)
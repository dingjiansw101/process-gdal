from osgeo import gdal
from osgeo import ogr
import numpy as np
import cv2

filename = r'E:\20170719-img8\GF2_PMS1_E23.4_N37.9_20160821_L1A0001776593\GF2_PMS1_E23.4_N37.9_20160821_L1A0001776593-MSS1.tiff'
dataset = gdal.Open(filename, gdal.GA_ReadOnly)
band = dataset.GetRasterBand(1)
XSize = dataset.RasterXSize
YSize = dataset.RasterYSize

img = dataset.ReadAsArray(0, 0, 1000, 1000)
img2 = np.uint8(img/4)
print np.shape(img2)
out = img2[0:3, 0: 1000, 0:1000]
print np.shape(out)
print 'out:', out
#cv2.imwrite(r'E:\20170719-img8\GF2_PMS1_E23.4_N37.9_20160821_L1A0001776593-MSS1-1000.tiff', out)

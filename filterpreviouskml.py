import os
import gdal
from parse_geotiff import fromtifgetextent
import utils as util
import shutil
from parsekml import parsekml

def calc_iou(extenta, extentb):
    xmin1, ymin1, xmax1, ymax1 = extenta[0], extenta[1], extenta[2], extenta[3]
    xmin2, ymin2, xmax2, ymax2 = extentb[0], extentb[1], extentb[2], extentb[3]

    inter_xmin = max(xmin1, xmin2)
    inter_xmax = min(xmax1, xmax2)
    inter_ymin = max(ymin1, ymin2)
    inter_ymax = min(ymax1, ymax2)

    inter_area = (inter_xmax - inter_xmin) * (inter_ymax - inter_ymin)
    area1 = (xmax1 - xmin1) * (ymax1 - ymin1)
    area2 = (xmax2 - xmin2) * (ymax2 - ymin2)

    iou = float(inter_area) / float(area1 + area2 - inter_area)
    return iou

def checkexist(newextent, extents):
    for extent in extents:
        if calc_iou(newextent, extent) > 0:
            return True
    return False

def allpreviousextents():
    filepath = r'/home/dingjian/Pictures/coord/91formerkml'
    extents = []
    filelist = util.GetFileFromThisRootDir(filepath)
    for filename in filelist:
        extent = parsekml(filename)
        extents.append(extent)
    return extents

def filecopy(srcpath, dstpath, filenames, extent):
    for name in filenames:
        srcdir = os.path.join(srcpath, name + extent)
        dstdir = os.path.join(dstpath, name + '.jpg')
        print('srcdir:', srcdir)
        print('dstdir:', dstdir)
        if os.path.exists(srcdir):
            shutil.copyfile(srcdir, dstdir)

def main():
    filepath = r'/home/dingjian/Pictures/harbor'
    outpath = r'/home/dingjian/Pictures/Filteredhabor'
    filelist = util.GetFileFromThisRootDir(filepath)
    extents = allpreviousextents()
    filterednames = []
    for filename in filelist:
        newextent = fromtifgetextent(filename)
        if not checkexist(newextent, extents):
            filterednames.append(filename)
    names = [util.mybasename(x) for x in filterednames]
    filecopy(filepath, outpath, names, '.tif')


if __name__ == '__main__':
    main()
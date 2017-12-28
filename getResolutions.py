import os
import utils as util
from parse_geotiff import parge_geotiff


def addresolution():
    basepath = r'E:\bod-dataset'
    imgpath = os.path.join(basepath, 'images')
    respath = os.path.join(basepath, 'resolution')
    diff = util.filesetcalc(imgpath, respath, 'd')
    for name in diff:
        outname = os.path.join(respath, name + '.txt')
        with open(outname, 'w') as f_out:
            if ('GF' in name):
                f_out.write('1')
            elif ('JL' in name):
                f_out.write('0.72')
def query(querypath, tifpath):
    queryfiles = util.GetListFromfile(querypath)
    queryimgs = {util.mybasename(x) for x in queryfiles}
    tiflist = util.GetListFromfile(tifpath, '.tif')
    tifdict = {util.mybasename(x): x for x in tiflist}
    for img in queryimgs:
        tifimg = tifdict[img]

def main():
    googlepath = r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date'
    imgpath = os.path.join(googlepath, 'images')
    files = util.GetFileFromThisRootDir(imgpath)
    chooseimgs = {util.mybasename(x) for x in files}
    origpath = r'E:\GoogleEarth\up-9-25-data'
    orignames = util.GetFileFromThisRootDir(origpath, '.tif')
    outpath = r'E:\bod-dataset\GooglePng'
    resolutionpath = r'E:\bod-dataset\resolution'
    translist = []
    for fullname in orignames:
        imgname = util.mybasename(fullname)
        if imgname in chooseimgs:
            print('name: ', imgname)
            if imgname not in translist:
                translist.append(imgname)
                resolution = parge_geotiff(fullname)
                outdir = os.path.join(resolutionpath, imgname + '.txt')
                with open(outdir, 'w') as f_out:
                    f_out.write(str(resolution) + '\n')

if __name__ == '__main__':
    addresolution()
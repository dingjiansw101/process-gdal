
import pandas as pd
from lxml import etree
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import ATOM_ElementMaker as ATOM
from pykml.factory import GX_ElementMaker as GX
import os
import codecs
import xml.etree.ElementTree as ET
import utils as util


## check duplication by extent

levels = {'15': 4.29153442383e-05, '16': 2.14576721191e-05, '17': 1.07288360596e-05, '18': 5.36441802979e-06, '19': 2.68220901489e-06}
selectlevel = '17'
imagesize = 4096

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

def test_iou():
    extenta = (1, 1, 2, 2)
    extentb = (1, 1, 2, 2)
    iou = calc_iou(extenta, extentb)
    print iou

def point2extent(location, level, pixsize):
  resolution = levels[level]
  lat, lon = location[0], location[1]
  halfsize = pixsize / 2
  xmin = lon - halfsize * resolution
  ymin = lat - halfsize * resolution
  xmax = lon + halfsize * resolution
  ymax = lat + halfsize * resolution
  extent = (xmin, ymin, xmax, ymax)
  return extent

def writeltsk(level, dstfile):
  with open(dstfile, 'w') as f:
    f.write(r'IMAGE======' + level + '======0')

def writekml(extent, dstfile):
  xmin, ymin, xmax, ymax = extent[0], extent[1], extent[2], extent[3]

  coord = (xmin, ymax,
           xmin, ymin,
           xmax, ymin,
           xmax, ymax)
  doc = KML.kml(
    KML.Document(
      KML.Placemark(
        KML.visibility('1'),
        KML.Style(
          KML.LineStyle(
            KML.color('cc0000ff'),
            KML.width('1'),
          ),
          KML.PolyStyle(
            KML.color('4c3f7fff'),
            KML.fill('1'),
            KML.outline('1'),
          ),
        ),
        KML.Polygon(
          KML.altitudeMode('clampToGround'),
          KML.outerBoundaryIs(
            KML.LinearRing(
              KML.coordinates(
                str(coord[0]) + ',' + str(coord[1]) + ' ' +
                str(coord[2]) + ',' + str(coord[3]) + ' ' +
                str(coord[4]) + ',' + str(coord[5]) + ' ' +
                str(coord[6]) + ',' + str(coord[7]) + ' ' +
                str(coord[0]) + ',' + str(coord[1]) + ' '
              ),
            ),
          ),
        ),
      ),
    ),
  )
  #print etree.tostring(etree.ElementTree(doc),pretty_print=True)
  # output a KML file (named based on the Python script)
  outfile = file(dstfile,'w')
  outfile.write(etree.tostring(doc, pretty_print=True))

def parse_airport_csv(filename):
  airportlist = pd.read_csv(r'E:\documentation\OneDrive\documentation\coordinates\airports.csv')
    # print airportlist
  print airportlist['Latitude']
  lats = airportlist['Latitude']
  lons = airportlist['Longitude']
  extents = []
  for i in range(len(lats)):
    lat = float(lats[i])
    lon = float(lons[i])
    extent = point2extent((lat, lon), selectlevel, imagesize)
    extents.append(extent)
  return extents

def ParseMarine(path):
    #path = r'E:\documentation\OneDrive\documentation\coordinates\marine_coord'
    filelist = util.GetFileFromThisRootDir(path)
    extents = []
    for filename in filelist:
        with open(filename, 'r') as f:
            lines = f.readlines()
            splitlines = [x.strip().split(' ') for x in lines]
            for splitline in splitlines:
                lat = float(splitline[1])
                lon = float(splitline[2])
                extent = point2extent((lat, lon), selectlevel, imagesize)
                extents.append(extent)
    return extents

def ParseHRSCcoord(basepath):
    filelist = util.GetFileFromThisRootDir(basepath, 'xml')
    extents = []
    ## for test
    #lats = []

    for filename in filelist:
        tree = ET.parse(filename)
        location = tree.find('Img_Location').text
        coord = location.split(',')
        coord = map(float, coord)
        print 'coord:', coord

        ## for test
        #lats.append(coord[0])

        extent = point2extent(coord, selectlevel, imagesize)
        extents.append(extent)

    ## for test
    #latset = set(lats)
    #print 'coord len:', len(latset)
    return extents

def testParseHRSC():
    extents = ParseHRSCcoord(r'E:\downloaddataset\HRSC2016\HRSC2016\HRSC2016\HRSC2016\FullDataSet\Annotations')
    print 'extent:', extents

## true represent exist duplication
def check_duplication(ExtentsSet, SingleExtent):
    for extent in ExtentsSet:
        if (calc_iou(extent, SingleExtent) > 0.2):
            return True
    return False

def parse_jinpu(filename):
  extents = []
  with open(filename, 'r') as f:
    lines = f.readlines()
    length = len(lines)
    for i in range(length/2):
      lat = float(lines[i * 2])
      lon = float(lines[i * 2 + 1])
      extent = point2extent((lat, lon), selectlevel, imagesize)

      extents.append(extent)
  return extents

def duplicatefilter(extents):
    #jinpu_extents = parse_jinpu(r'G:\LocaSpaceViewer\LocaSpaceViewer\download\coordinates\airport.txt')
    HRSC_extents = ParseHRSCcoord(r'E:\downloaddataset\HRSC2016\HRSC2016\HRSC2016\HRSC2016\FullDataSet\Annotations')
    exist_extents = HRSC_extents
    #marine12_extents = ParseMarine(r'E:\documentation\OneDrive\documentation\coordinates\marine_coord')
    #exist_extents = HRSC_extents + marine12_extents

    outextents = []
    for extent in extents:
        if (not check_duplication(exist_extents, extent)):
            outextents.append(extent)
        else:
            print 'duplicate:', extent

    return outextents

def main():
    #filename = r'E:\documentation\OneDrive\documentation\coordinates\airports.csv'
    #extents = parse_airport_csv(filename)
    #filepath = r'E:\documentation\OneDrive\documentation\coordinates\marine_coord'
    filepath = r'E:\documentation\OneDrive\documentation\coordinates\marine_coord'
    extents = ParseMarine(filepath)
    print 'len extents:', len(extents)
    filtered_extents = duplicatefilter(extents)
    print 'len filtered_extents:', len(filtered_extents)

    filtered_extents = list(set(x for x in filtered_extents))
    print 'set filtered_extents:', len(filtered_extents)

    for index, extent in enumerate(filtered_extents):
        writekml(extent, os.path.join(r'E:\documentation\OneDrive\documentation\coordinates\marine_kml12_level17',
                                      str(index) + '.kml'))
        writeltsk(selectlevel, os.path.join(r'E:\documentation\OneDrive\documentation\coordinates\marine_kml12_level17',
                                            str(index) + '.ltsk'))

if __name__ == '__main__':
    main()
    # testParseHRSC()
from lxml import etree
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import ATOM_ElementMaker as ATOM
from pykml.factory import GX_ElementMaker as GX
import os

levels = {'16': 2.14576721191e-05, '17': 1.07288360596e-05, '18': 5.36441802979e-06, '19': 2.68220901489e-06}
selectlevel = '16'

# lat:weidu, lon:jingdu
def point2extent(location, level, pixsize):
  resolution = levels[level]
  lat, lon = location[0], location[1]
  halfsize = pixsize / 2
  xmin = lon - halfsize * resolution
  ymin = lat - halfsize * resolution
  xmax = lon + halfsize * resolution
  ymax = lat + halfsize * resolution
  extent = [xmin, ymin, xmax, ymax]
  return extent

def writeltsk(level, dstfile):
  with open(dstfile, 'w') as f:
    f.write(r'IMAGE======' + level + '======0')

## extent = (xmin, ymin, xmax, ymax)
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
  print etree.tostring(etree.ElementTree(doc),pretty_print=True)
  # output a KML file (named based on the Python script)
  outfile = file(dstfile,'w')
  outfile.write(etree.tostring(doc, pretty_print=True))
def parse_jinpu(filename):
  extents = []
  with open(filename, 'r') as f:
    lines = f.readlines()
    length = len(lines)
    for i in range(length/2):
      lat = float(lines[i * 2])
      lon = float(lines[i * 2 + 1])
      extent = point2extent((lat, lon), selectlevel, 1024)

      extents.append(extent)
  return extents
def main():
  filename = r'G:\LocaSpaceViewer\LocaSpaceViewer\download\coordinates\airport.txt'
  extents = parse_jinpu(filename)
  for index, extent in enumerate(extents):
    writekml(extent, os.path.join(r'G:\LocaSpaceViewer\LocaSpaceViewer\download\coordinates',
                                  str(index) + '.kml'))
    writeltsk(selectlevel, os.path.join(r'G:\LocaSpaceViewer\LocaSpaceViewer\download\coordinates',
                                  str(index) + '.ltsk'))
if __name__ == '__main__':
  main()
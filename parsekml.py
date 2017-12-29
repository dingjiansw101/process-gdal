# -*- coding: utf-8 -*-
from os import path
from pykml import parser
from bs4 import BeautifulSoup
from bs4 import element
import xml.etree.ElementTree as ET
import numpy as np
import re


def parsekml(filename):
    def coord2extent(coords):
        # xmin = np.min(coords, axis=0)
        # ymin = np.min(coords, axis=1)
        # xmax = np.max(coords, axis=0)
        # ymax = np.max(coords, axis=1)


        # print 'points:', points
        coordinates = coords.text
        pattern = re.compile(r'([0-9-\.]+),([0-9-\.]+),0')
        points = re.findall(pattern, coordinates)
        xs = [float(x[0]) for x in points]
        ys = [float(x[1]) for x in points]

        xmin = np.min(xs)
        xmax = np.max(xs)
        ymin = np.min(ys)
        ymax = np.max(ys)
        extent = (xmin, ymin, xmax, ymax)

        print 'points:', points
        return extent
    root = parser.fromstring(open(filename).read())
    coordinates = root.Document.Folder.Placemark.Polygon.outerBoundaryIs.LinearRing.coordinates


    extent = coord2extent(coordinates)
    print 'coordinates:', coordinates
    print 'extent:', extent
    return extent

def main():
    parsekml('/home/dingjian/Pictures/coord/91formerkml/322114_任务范围.kml')

    # root = parser.fromstring(open('/home/dingjian/Pictures/coord/91formerkml/322114_任务范围.kml').read())
    # print root.Document.Folder.Placemark.Polygon.outerBoundaryIs.LinearRing.coordinates
if __name__ == '__main__':
    main()
from pyproj import Proj, transform
from parse_geotiff import parge_geotiff

def mycoordTrans(srcepsg, dstdatum, coord):
    # define the projections
    p1 = Proj(init=srcepsg)
    p2 = Proj(proj='latlong', datum=dstdatum)

    ##
    x_degree, y_degree = p1(coord[0], coord[1], inverse=True)
    print 'x_degree:', x_degree
    print 'y_degree:', y_degree
    # Transform point (155000.0, 446000.0) with EPSG:28992
    lon, lat, z = transform(p1, p2, coord[0], coord[1], coord[2])
    return lon, lat, z  # 5.38720294616 52.0023756348 43.6057764404

def getlonlat(filename):
    resolution, origin, XSize, YSize = parge_geotiff(filename)
    ## need to check the type of projection
    coord = [origin[0], origin[1], 0]
    lon, lat, z = mycoordTrans(r'EPSG:2386',
                             r'WGS84',
                             coord)
    return lon, lat, z
## wrong
#filename = r'E:\GoogleEarth\dingjian\car\images\yuyi3.tif'

## ok
#filename = r'E:\GoogleEarth\singapore\images\singapore-2016-4-27-1.tif'

## wrong
filename = r'E:\013022223103.tif'

long, lat, z = getlonlat(filename)
print 'long:', long, ' lat:', lat
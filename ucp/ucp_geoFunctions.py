import os.path as opath
from functools import reduce
from shapely.geometry import Polygon, Point

geo_dpath = reduce(opath.join,
               [opath.dirname(opath.realpath(__file__)),
                '..', '..', 'taxi_data', 'geo'])
kml_fpath = opath.join(geo_dpath, 'queues.kml')
apPolygons_fpath = 'apPolygons.txt'


def extract_ap_polygons():
    from pykml import parser
    #
    with open(kml_fpath) as f:
        kml_doc = parser.parse(f).getroot().Document
    poly_names = ['T1', 'T2', 'T3', 'BudgetT']
    with open(apPolygons_fpath, 'w') as f:
        for pm in kml_doc.Placemark:
            if pm.name in poly_names:
                str_coords = str(pm.Polygon.outerBoundaryIs.LinearRing.coordinates)
                points = []
                for l in ''.join(str_coords.split()).split(',0')[:-1]:
                    _long, _lat = l.split(',')
                    points.append([eval(_long), eval(_lat)])
                f.write('%s:%s\n' % (pm.name, str(points)))


def get_ap_polygons():
    ap_polygons = []
    with open(apPolygons_fpath, 'r') as f:
        contents = f.readlines()
    for l in contents:
        terName, _polyCoords = l.rstrip('\n').split(':')
        ap_poly = poly(eval(_polyCoords))
        ap_poly.name = terName
        ap_polygons.append(ap_poly)
    return ap_polygons


class poly(Polygon):
    def __init__(self, poly_points):
        Polygon.__init__(self, poly_points)

    def is_including(self, coordinate):
        assert type(coordinate) == type(()), coordinate
        assert len(coordinate) == 2, len(coordinate)
        p = Point(*coordinate)
        return p.within(self)


if __name__ == '__main__':
    # extract_ap_polygons()
    ap_polygons = get_ap_polygons()


    end_lon = 103.98973687999998
    end_lat = 1.3611000837999998

    # end_lon, end_lat = 103.9888924, 1.362931656

    apBasePos = 'X'
    for ap_polygon in ap_polygons:
        if ap_polygon.is_including((end_lon, end_lat)):
            apBasePos = ap_polygon.name
            break
    print(apBasePos)

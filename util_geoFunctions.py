from __path_organizer import *
#
#
from pykml import parser
from shapely.geometry import Polygon, Point


def get_ap_polygons():
    poly_names = ['T1', 'T2', 'T3', 'BudgetT']
    kml_doc = None
    ifpath = opath.join(dpath['geo'], 'queues.kml')
    with open(ifpath) as f:
        kml_doc = parser.parse(f).getroot().Document
    ap_polygons = []
    for pm in kml_doc.Placemark:
        if pm.name in poly_names:
            str_coords = str(pm.Polygon.outerBoundaryIs.LinearRing.coordinates)
            points = []
            for l in ''.join(str_coords.split()).split(',0')[:-1]:
                _long, _lat = l.split(',')
                points.append([eval(_long), eval(_lat)])
            ap_poly = poly(points)
            ap_poly.name = pm.name if pm.name != 'BudgetT' else 'B'
            ap_polygons.append(ap_poly)
    return ap_polygons


def get_ns_polygon():
    kml_doc = None
    ifpath = opath.join(dpath['geo'], 'queues.kml')
    with open(ifpath) as f:
        kml_doc = parser.parse(f).getroot().Document
    for pm in kml_doc.Placemark:
        if pm.name == 'Night Safari':
            str_coords = str(pm.Polygon.outerBoundaryIs.LinearRing.coordinates)
            points = []
            for l in ''.join(str_coords.split()).split(',0')[:-1]:
                _long, _lat = l.split(',')
                points.append([eval(_long), eval(_lat)])
            return poly(points)


class poly(Polygon):
    def __init__(self, poly_points):
        Polygon.__init__(self, poly_points)

    def is_including(self, coordinate):
        assert type(coordinate) == type(()), coordinate
        assert len(coordinate) == 2, len(coordinate)
        p = Point(*coordinate)
        return p.within(self)


if __name__ == '__main__':
    pass

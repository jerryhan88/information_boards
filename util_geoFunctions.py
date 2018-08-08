import os.path as opath
import pickle
from shapely.geometry import Polygon, Point
#
from __path_organizer import geo_dpath
#


def get_ap_polygons():
    fpath = opath.join(geo_dpath, 'terminalPoly.pkl')
    if not opath.exists(fpath):
        from pykml import parser
        poly_names = ['T1', 'T2', 'T3', 'BudgetT']
        ifpath = opath.join(geo_dpath, 'queues.kml')
        with open(ifpath) as f:
            kml_doc = parser.parse(f).getroot().Document
        assert kml_doc is not None
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
        with open(fpath, 'wb') as fp:
            pickle.dump(ap_polygons, fp)
    else:
        with open(fpath, 'rb') as fp:
            ap_polygons = pickle.load(fp)
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
    get_ap_polygons()

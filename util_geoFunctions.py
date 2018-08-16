import os.path as opath
import pickle
from shapely.geometry import Polygon, Point
#
from __path_organizer import geo_dpath
#


def get_ap_polygons():
    fpath = opath.join(geo_dpath, 'terminalCoords.pkl')
    if not opath.exists(fpath):
        from pykml import parser
        terminal_coords = {}
        poly_names = ['T1', 'T2', 'T3', 'BudgetT']
        ifpath = opath.join(geo_dpath, 'queues.kml')
        with open(ifpath) as f:
            kml_doc = parser.parse(f).getroot().Document
        assert kml_doc is not None
        for pm in kml_doc.Placemark:
            if pm.name in poly_names:
                str_coords = str(pm.Polygon.outerBoundaryIs.LinearRing.coordinates)
                points = []
                for l in ''.join(str_coords.split()).split(',0')[:-1]:
                    _lng, _lat = l.split(',')
                    points.append([eval(_lng), eval(_lat)])
                terminal_coords[pm.name if pm.name != 'BudgetT' else 'B'] = points
        with open(fpath, 'wb') as fp:
            pickle.dump(terminal_coords, fp)
    else:
        with open(fpath, 'rb') as fp:
            terminal_coords = pickle.load(fp)
    ap_polygons = []
    for tn, points in terminal_coords.items():
        ap_poly = poly(points)
        ap_poly.name = tn
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
    print(get_ap_polygons())

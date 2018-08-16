

import sys
from shapely.geometry import Polygon, Point
#
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import (QPainter, QFont, QPen,
                         QImage, QPalette)
from PyQt5.QtCore import Qt, QSize, QRectF, QSizeF
#
from sgDistrict import get_sgBorder, get_distPoly
from util_geoFunctions import get_ap_polygons



sgBorder = get_sgBorder()
min_lng, max_lng = 1e400, -1e400
min_lat, max_lat = 1e400, -1e400
for poly in sgBorder:
    for lat, lng in poly:
        if lng < min_lng:
            min_lng = lng
        if lng > max_lng:
            max_lng = lng
        if lat < min_lat:
            min_lat = lat
        if lat > max_lat:
            max_lat = lat
lng_gap = max_lng - min_lng
lat_gap = max_lat - min_lat


WIDTH = 1800.0
# WIDTH = 800.0
HEIGHT = lat_gap * (WIDTH / lng_gap)

FRAME_ORIGIN = (60, 100)



def convert_GPS2xy(lng, lat):
    x = (lng - min_lng) / lng_gap * WIDTH
    y = (max_lat - lat) / lat_gap * HEIGHT
    return x, y


class Viz(QWidget):
    def __init__(self):
        super().__init__()
        self.app_name = 'Viz'
        self.objForDrawing = []
        #
        self.init_bgDrawing()
        self.initUI()

    def initUI(self):
        self.setGeometry(FRAME_ORIGIN[0], FRAME_ORIGIN[1], WIDTH, HEIGHT)
        self.setWindowTitle(self.app_name)
        self.setFixedSize(QSize(WIDTH, HEIGHT))
        #
        self.image = QImage(WIDTH, HEIGHT, QImage.Format_RGB32)
        self.image.fill(Qt.white)
        pal = self.palette()
        pal.setColor(QPalette.Background, Qt.white)
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        #
        self.show()

    def init_bgDrawing(self):
        sgBoarderXY = []
        for poly in sgBorder:
            sgBorderPartial_xy = []
            for lat, lng in poly:
                x, y = convert_GPS2xy(lng, lat)
                sgBorderPartial_xy += [(x, y)]
            sgBoarderXY.append(sgBorderPartial_xy)
        sgDistrictXY = {}
        distPoly = get_distPoly()
        for dist_name, poly in distPoly.items():
            points = []
            for lat, lng in poly:
                points.append(convert_GPS2xy(lng, lat))
            sgDistrictXY[dist_name] = points
        self.sg = Singapore(sgBoarderXY, sgDistrictXY)
        self.objForDrawing = [self.sg]
        #
        ap_polygons = get_ap_polygons()
        for poly in ap_polygons:
            points = []
            for lng, lat in list(poly.boundary.coords):
                points.append(convert_GPS2xy(lng, lat))
            self.objForDrawing.append(Terminal(poly.name, points))

    def paintEvent(self, e):
        for canvas in [self, self.image]:
            qp = QPainter()
            qp.begin(canvas)
            self.drawCanvas(qp)
            qp.end()

    def drawCanvas(self, qp):
        for o in self.objForDrawing:
            o.draw(qp)

    def save_img(self, img_fpath):
        assert img_fpath.endswith('.png')
        self.image.save(img_fpath, 'png')


class Terminal(object):
    def __init__(self, tn, polyCoords):
        self.tn = tn
        self.polyCoords = polyCoords

    def draw(self, qp):
        pen = QPen(Qt.red, 0.5)
        qp.setPen(pen)
        for i in range(len(self.polyCoords) - 1):
            x0, y0 = self.polyCoords[i]
            x1, y1 = self.polyCoords[i + 1]
            qp.drawLine(x0, y0, x1, y1)


class Singapore(object):
    def __init__(self, sgBoarderXY, sgDistrictXY):
        self.sgBoarderXY = sgBoarderXY
        self.sgDistrictXY = sgDistrictXY
        self.sgDistrictPolyXY = {}
        for dist_name, points in self.sgDistrictXY.items():
            self.sgDistrictPolyXY[dist_name] = Polygon(points)

    def get_distName(self, x, y):
        p0 = Point(x, y)
        for dist_name, poly in self.sgDistrictPolyXY.items():
            if p0.within(poly):
                return dist_name
        else:
            return None

    def drawPoly(self, qp, poly):
        for i in range(len(poly) - 1):
            x0, y0 = poly[i]
            x1, y1 = poly[i + 1]
            qp.drawLine(x0, y0, x1, y1)
        x0, y0 = poly[len(poly) - 1]
        x1, y1 = poly[0]
        qp.drawLine(x0, y0, x1, y1)

    def draw(self, qp):
        pen = QPen(Qt.black, 0.2, Qt.DashLine)
        qp.setPen(pen)
        for dist_name, poly in self.sgDistrictXY.items():
            self.drawPoly(qp, poly)
        pen = QPen(Qt.black, 1)
        qp.setPen(pen)
        for _, poly in enumerate(self.sgBoarderXY):
            self.drawPoly(qp, poly)



if __name__ == '__main__':
    viz_fpath = 'temp.png'
    #
    app = QApplication(sys.argv)
    viz = Viz()
    viz.save_img(viz_fpath)
    sys.exit(app.exec_())
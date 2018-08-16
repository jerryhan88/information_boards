import os.path as opath
import sys
import csv
from datetime import datetime
from shapely.geometry import Polygon, Point
#
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import (QPainter, QFont, QPen, QColor,
                         QImage, QPalette)
from PyQt5.QtCore import Qt, QSize, QRectF, QSizeF
from colour import Color
#
from sgDistrict import get_sgBorder, get_distPoly
from util_geoFunctions import get_ap_polygons
#
from __path_organizer import viz_dpath


pallet = [
    Color('blue').get_hex_l(),  # FREE
    Color('brown').get_hex_l(),
    Color('magenta').get_hex_l(),
    Color('green').get_hex_l(),
    Color('indigo').get_hex_l(),
    Color('red').get_hex_l(),  # POS
    Color('khaki').get_hex_l(),
    Color('maroon').get_hex_l(),
    Color('navy').get_hex_l(),  # PAYMENT
    Color('orange').get_hex_l(),
    Color('pink').get_hex_l(),
    Color('grey').get_hex_l(),
]


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
Traj_dotSize = 2
TE_MARKER_SIZE = 10



def convert_GPS2xy(lng, lat):
    x = (lng - min_lng) / lng_gap * WIDTH
    y = (max_lat - lat) / lat_gap * HEIGHT
    return x, y


class Viz(QWidget):
    def __init__(self, fpaths=None):
        super().__init__()
        self.app_name = 'Viz'
        self.fpaths = fpaths
        self.objForDrawing = []
        #
        self.init_drawing()
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

    def init_drawing(self):
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
        if self.fpaths:
            with open(self.fpaths['tripF']) as r_csvfile:
                reader = csv.DictReader(r_csvfile)
                for row in reader:
                    pLat, pLng = map(eval, [row[cn] for cn in ['previous_dropoff_latitude', 'previous_dropoff_longitude']])
                    sLat, sLng = map(eval, [row[cn] for cn in ['start_latitude', 'start_longitude']])
                    eLat, eLng = map(eval, [row[cn] for cn in ['end_latitude', 'end_longitude']])
                    tPrev, tStart, tEnd = map(eval, [row[cn] for cn in ['time_previous_dropoff', 'start_time', 'end_time']])
                    tEnter, tExit, tFree = map(eval, [row[cn] for cn in ['time_enter_airport', 'time_exit_airport', 'time_first_free']])
            dt_tPrev, dt_tEnter, dt_tStart, dt_tExit, dt_tEnd, dt_tFree = map(datetime.fromtimestamp,
                                                                    [tPrev, tEnter, tStart, tExit, tEnd, tFree])
            trip_events = {
                'P': [dt_tPrev, convert_GPS2xy(pLng, pLat)],
                'S': [dt_tStart, convert_GPS2xy(sLng, sLat)],
                'E': [dt_tEnd, convert_GPS2xy(eLng, eLat)],
            }
            logs = []
            with open(self.fpaths['logF']) as r_csvfile:
                reader = csv.DictReader(r_csvfile)
                for row in reader:
                    state, lng, lat = map(eval, [row[cn] for cn in ['state', 'lng', 'lat']])
                    x, y = convert_GPS2xy(lng, lat)
                    logs.append((state, x, y))
                    #
                    t = eval(row['time'])
                    if t == tEnter:
                        trip_events['EN'] = [dt_tEnter, (x, y)]
                    if t == tExit:
                        trip_events['EX'] = [dt_tExit, (x, y)]
                    if t == tFree:
                        trip_events['F'] = [dt_tFree, (x, y)]
            for en in ['EN', 'EX', 'F']:
                assert en in trip_events
            self.objForDrawing.append(Trajectory(trip_events, logs))


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


class Trajectory(object):

    T_X, T_Y = WIDTH * 0.5, HEIGHT * 0.5

    def __init__(self, trip_events, logs):
        self.logs = logs
        self.trip_events = trip_events

    def set_penByState(self, state, qp):
        pen_color = QColor(pallet[state])
        pen = QPen(pen_color, 1, Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(pen_color)

    def draw(self, qp):
        ps, px, py = None, -1, -1
        for i, (cs, cx, cy) in enumerate(self.logs):
            if i == 0:
                self.set_penByState(cs, qp)
            else:
                qp.drawLine(px, py, cx, cy)
            if ps != cs:
                self.set_penByState(cs, qp)
            qp.drawEllipse(cx - Traj_dotSize / 2, cy - Traj_dotSize / 2,
                           Traj_dotSize, Traj_dotSize)
            ps, px, py = cs, cx, cy

        pen = QPen(Qt.black, 1, Qt.SolidLine)
        qp.setPen(pen)
        for en, (et, (cx, cy)) in self.trip_events.items():
            for x0, y0, x1, y1 in [
                (cx, cy, cx + TE_MARKER_SIZE, cy + TE_MARKER_SIZE),
                (cx + TE_MARKER_SIZE, cy, cx, cy + TE_MARKER_SIZE),
            ]:
                qp.drawLine(x0, y0, x1, y1)
            if en == 'P':
                qp.drawText(Trajectory.T_X, Trajectory.T_Y, en)

                qp.drawLine(Trajectory.T_X, Trajectory.T_Y, cx, cy)
            else:
                qp.drawText(cx, cy, en)

            #


class Terminal(object):
    def __init__(self, tn, polyCoords):
        self.tn = tn
        self.polyCoords = polyCoords

    def draw(self, qp):
        pen = QPen(QColor(Color('brown').get_hex_l()), 0.5, Qt.DashDotLine)
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
    fpaths = {'logF': opath.join(viz_dpath, 'XAX-log.csv'),
              'tripF': opath.join(viz_dpath, 'XAX-trip.csv')}
    #
    app = QApplication(sys.argv)
    viz = Viz(fpaths)
    viz.save_img(viz_fpath)
    sys.exit(app.exec_())
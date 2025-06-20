from networkx.classes import selfloop_edges
from qgis.gui import QgsMapToolEmitPoint, QgisInterface, QgsMapCanvas, QgsMapMouseEvent, QgsRubberBand, QgsGeometryRubberBand, Qgis
from qgis.core import QgsPointXY, QgsGeometry
from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtGui import QColor

from .coord import CoordUtils, PolarCoord, CartesianCoord
from .vehicle import Vehicle


class VehiclePlacer(QgsMapToolEmitPoint):
    placed = pyqtSignal(name="VehiclePlaced")

    def __init__(self, iface: QgisInterface, vehicle: Vehicle):
        self._iface: QgisInterface = iface
        self._vehicle: Vehicle = vehicle

        self._canvas: QgsMapCanvas = iface.mapCanvas()
        QgsMapToolEmitPoint.__init__(self, self._canvas)

        # Base point and rotation
        self._base_point: CartesianCoord = CartesianCoord(0.0, 0.0)
        self._rotation: float = 0

        self._click_counter = 0
        self._marker = QgsRubberBand(self._canvas, Qgis.GeometryType.Polygon)


    def canvasPressEvent(self, e: QgsMapMouseEvent):
        if e.button() == Qt.LeftButton:
            self._position_clicked(self.toMapCoordinates(e.pos()))

        if e.button() == Qt.RightButton:
            self._finish_clicked()


    def canvasMoveEvent(self, e: QgsMapMouseEvent):
        position = self.toMapCoordinates(e.pos())
        if self._click_counter == 0:
            self._set_base_point(position)
            self._vehicle.place_vehicle(self._base_point, self._rotation)
            self._draw_marker()
        else:
            self._set_rotation(position)
            self._vehicle.place_vehicle(self._base_point, self._rotation)
            self._draw_marker()


    def _position_clicked(self, position: QgsPointXY):
        if self._click_counter == 0:
            self._vehicle.place_vehicle(self._base_point, self._rotation)
            self._draw_marker()
            self._click_counter += 1
        else:
            self._set_rotation(position)
            self._vehicle.place_vehicle(self._base_point, self._rotation)
            self._draw_marker()
            self._click_counter = 0


    def _set_rotation(self, position: QgsPointXY):
        self._rotation = CoordUtils.to_polar(
            dx=position.x() - self._base_point.x,
            dy=position.y() - self._base_point.y
        ).a


    def _set_base_point(self, position):
        self._base_point: CartesianCoord = CartesianCoord(
            x=position.x(),
            y=position.y()
        )


    def _draw_marker(self):
        self._canvas.scene().removeItem(self._marker)
        self._marker = QgsRubberBand(self._canvas, Qgis.GeometryType.Polygon)  # True = a polygon
        points = [[
            QgsPointXY(self._vehicle.fl.x, self._vehicle.fl.y),
            QgsPointXY(self._vehicle.bl.x, self._vehicle.bl.y),
            QgsPointXY(self._vehicle.br.x, self._vehicle.br.y),
            QgsPointXY(self._vehicle.fr.x, self._vehicle.fr.y)
        ]]

        self._marker.setToGeometry(QgsGeometry.fromPolygonXY(points), None)
        self._marker.setStrokeColor(QColor(255, 0, 0))
        self._marker.setWidth(3)


    def _finish_clicked(self):
        self._canvas.scene().removeItem(self._marker)
        self._click_counter = 0
        self._iface.actionPan().trigger()
        self.placed.emit()

    def deactivate(self):
        self._canvas.scene().removeItem(self._marker)
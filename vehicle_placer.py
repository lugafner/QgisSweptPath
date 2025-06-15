from networkx.classes import selfloop_edges
from qgis.gui import QgsMapToolEmitPoint, QgisInterface, QgsMapCanvas, QgsMapMouseEvent, QgsMapToolPan
from qgis.core import QgsPointXY
from qgis.PyQt.QtCore import Qt, pyqtSignal

from .coord import CoordUtils, PolarCoord, CartesianCoord
from .vehicle import Vehicle


class VehiclePlacer(QgsMapToolEmitPoint):
    placed = pyqtSignal(Vehicle, name="VehiclePlaced")

    def __init__(self, iface: QgisInterface, vehicle: Vehicle):
        self._iface: QgisInterface = iface
        self._canvas: QgsMapCanvas = iface.mapCanvas()
        self._vehicle: Vehicle = vehicle

        # First and second point
        self._base_point: QgsPointXY = QgsPointXY(0.0, 0.0)
        self._rotation_point: QgsPointXY = QgsPointXY(1.0, 0.0)
        self._click_counter = 0

        QgsMapToolEmitPoint.__init__(self, self._canvas)


    def canvasPressEvent(self, e: QgsMapMouseEvent):
        if e.button() == Qt.LeftButton:
            self._set_clicked_coordinate(self.toMapCoordinates(e.pos()))

        if e.button() == Qt.RightButton:
            self._place()


    def _set_clicked_coordinate(self, position: QgsPointXY):
        if self._click_counter == 0:
            # Set base point coordinate
            self._base_point = position
            self._click_counter += 1
        else:
            # Set rotation point coordinate
            self._rotation_point = position
            self._click_counter = 0


    def _place(self):
        rotation_polar: PolarCoord = CoordUtils.to_polar(
            dx=self._rotation_point.x() - self._base_point.x(),
            dy=self._rotation_point.y() - self._base_point.y()
        )
        position_cartesian: CartesianCoord = CartesianCoord(
            x=self._base_point.x(),
            y=self._base_point.y()
        )

        self._vehicle.place_vehicle(position_cartesian, rotation_polar.a)
        self.placed.emit(self._vehicle)

    @property
    def vehicle(self) -> Vehicle:
        """Get the vehicle"""
        return self._vehicle

    @vehicle.setter
    def vehicle(self, v):
        """Set a new vehicle"""
        self._vehicle = v

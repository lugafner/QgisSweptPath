from networkx.classes import selfloop_edges
from qgis.gui import QgsMapToolEmitPoint, QgisInterface, QgsMapCanvas, QgsMapMouseEvent, QgsRubberBand, QgsGeometryRubberBand, Qgis
from qgis.core import QgsPointXY, QgsGeometry
from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtGui import QColor

from .coord import CoordUtils, PolarCoord, CartesianCoord
from .vehicle import Vehicle


class VehiclePlacer(QgsMapToolEmitPoint):
    """
    Qgis MapTool for placing the vehicle
    """
    placed = pyqtSignal(name="VehiclePlaced")

    def __init__(self, iface: QgisInterface, vehicle: Vehicle):
        """
        Constructor for a new VehiclePlacer

        @param iface: QgisInterface
        @param vehicle: The vehicle to be placed
        """
        self._iface: QgisInterface = iface
        self._vehicle: Vehicle = vehicle
        self._canvas: QgsMapCanvas = iface.mapCanvas()
        QgsMapToolEmitPoint.__init__(self, self._canvas)

        # Base point and rotation
        self._base_point: CartesianCoord = CartesianCoord(0.0, 0.0)
        self._rotation: float = 0

        # Click counter:
        # 0 (first left mouse click) = vehicle base point
        # 1 (second mouse click) = second point for calculate vehicle rotation
        self._click_counter = 0

        # Marker to show the main vehicle part during placement
        self._marker = QgsRubberBand(self._canvas, Qgis.GeometryType.Polygon)


    def canvasPressEvent(self, e: QgsMapMouseEvent):  # Signature warning can be ignored
        """
        Event when a mouse button is pressed
        @param e: QgsMapMouseEvent
        """
        if e.button() == Qt.LeftButton:
            # When the left button is clicked switch between place and rotate mode
            self._position_clicked()

        if e.button() == Qt.RightButton:
            # Finish vehicle placement, when the right button is clicked
            self._finish_clicked()


    def canvasMoveEvent(self, e: QgsMapMouseEvent):  # Signature warning can be ignored
        """
        Event when the mouse is moved
        Used to update the rubber band showing the current position
        @param e: QgsMapMouseEvent
        """
        position = self.toMapCoordinates(e.pos())
        if self._click_counter == 0:
            # If the click counter is 0, the vehicle base point will be moved
            self._set_base_point(position)
            self._vehicle.place_vehicle(self._base_point, self._rotation)
            self._draw_marker()
        else:
            # Else the rotation is recalculated
            self._set_rotation(position)
            self._vehicle.place_vehicle(self._base_point, self._rotation)
            self._draw_marker()


    def _position_clicked(self):
        """
        Update the click counter after the left mouse button is clicked
        to switch between place and rotate mode
        """
        if self._click_counter == 0:
            self._click_counter = 1 # Set counter to 1 to rotate the vehicle
        else:
            self._click_counter = 0  # Set counter to 0 for placing the vehicle again


    def _set_rotation(self, position: QgsPointXY):
        """
        Set the rotation field
        @param position: The last pointer position as map coordinate
        """
        self._rotation = CoordUtils.to_polar(
            dx=position.x() - self._base_point.x,
            dy=position.y() - self._base_point.y
        ).a


    def _set_base_point(self, position):
        """
        Set the base point field
        @param position: The last pointer position as map coordinate
        """
        self._base_point = CartesianCoord(
            x=position.x(),
            y=position.y()
        )


    def _draw_marker(self):
        """
        Draw the polygon marker to show the current vehicle position/rotation
        """
        self._canvas.scene().removeItem(self._marker)  # Remove old marker first
        self._marker = QgsRubberBand(self._canvas, Qgis.GeometryType.Polygon)
        # list of the corner points from the vehicle
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
        """
        Method is called, when the right mouse button is pressed
        The placement process will be stopped
        """
        self._vehicle.steering_angle = 0
        self._canvas.scene().removeItem(self._marker)  # Remove the rubber band
        self._click_counter = 0  # Set click counter to always start with positioning
        self.placed.emit()  # Emit the signal, that the vehicle is placed


    def deactivate(self):
        self._click_counter = 0  # Set click counter to always start with positioning
        self._canvas.scene().removeItem(self._marker)  # Remove the rubber band
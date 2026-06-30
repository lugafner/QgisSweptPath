from qgis.gui import QgsMapToolEmitPoint, QgisInterface, QgsMapCanvas, QgsMapMouseEvent, QgsRubberBand
from qgis.core import QgsPointXY, QgsGeometry, Qgis
from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtGui import QColor, QKeyEvent

from .coord import CoordUtils, CartesianCoord
from .vehicle import Vehicle


class VehiclePlacer(QgsMapToolEmitPoint):
    """
    Qgis MapTool for placing the vehicle
    """
    placed = pyqtSignal(name="VehiclePlaced")
    aborted = pyqtSignal(name="VehiclePlacementAborted")

    def __init__(self, iface: QgisInterface,
                 vehicle: Vehicle,
                 init_rotation: float = 0.0,
                 init_position: CartesianCoord = CartesianCoord(0, 0)):
        """
        Constructor for a new VehiclePlacer

        @param iface: QgisInterface
        @param vehicle: The vehicle to be placed
        @param init_rotation: The rotation used for initialise the placement. Default 0.0
        @param init_position: The position used for initialise the placement. Default 0, 0
        """
        self._iface: QgisInterface = iface
        self._vehicle: Vehicle = vehicle
        self._canvas: QgsMapCanvas = iface.mapCanvas()
        QgsMapToolEmitPoint.__init__(self, self._canvas)

        # Base point and rotation
        self._base_point: CartesianCoord = init_position
        self._rotation: float = init_rotation

        self._old_base_point: CartesianCoord = self._vehicle.f
        self._old_rotation: float = self._vehicle.a

        # Click counter:
        # 0 (first left mouse click) = vehicle base point
        # 1 (second mouse click) = second point for calculate vehicle rotation
        self._click_counter = 0

        # Marker to show the main vehicle part during placement
        self._marker = QgsRubberBand(self._canvas, Qgis.GeometryType.Polygon)

        # If the position is the init value, the click counter is set to 1 for movement
        # Else if a last position was present, the click counter is set to 0 so the vehicle could be placed on same position
        if self._base_point == CartesianCoord(0, 0):
            self._click_counter = 1
        else:
            self._vehicle.place_vehicle(self._base_point, self._rotation, floating=True)
            self._draw_marker()


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
            # If the click counter is 0, the vehicle will not be moved or rotatet
            pass
        elif self._click_counter == 1:
            # If the click counter is 1, the vehicle base point will be moved
            self._set_base_point(position)
            self._vehicle.place_vehicle(self._base_point, self._rotation, floating=True)
            self._draw_marker()
        else:
            # Else the rotation is recalculated
            self._set_rotation(position)
            self._vehicle.place_vehicle(self._base_point, self._rotation, floating=True)
            self._draw_marker()


    def keyPressEvent(self, e: QKeyEvent):
        """
        Event when a key is pressed
        Used to exit the placer tool
        @param e: QKeyEvent
        """
        if e.key() == Qt.Key_Escape:
            self._abort_placement()


    def _position_clicked(self):
        """
        Update the click counter after the left mouse button is clicked
        to switch between place and rotate mode
        """
        if self._click_counter == 0:
            self._click_counter = 1 # Set counter to 1 to move the vehicle
        elif self._click_counter == 1:
            self._click_counter = 2 # Set counter to 2 to rotate the vehicle
        else:
            self._click_counter = 1  # Set counter to 1 for placing the vehicle again


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
        self._vehicle.place_vehicle(self._base_point, self._rotation, floating=False)
        self._vehicle.steering_angle = 0.0
        self._vehicle.speed = 0.0
        self._canvas.scene().removeItem(self._marker)  # Remove the rubber band
        self._click_counter = 0  # Set click counter to always start with positioning
        self.placed.emit()  # Emit the signal, that the vehicle is placed


    def _abort_placement(self):
        """
        Method is called, when the Escape key is pressed
        The placement process will be stopped
        The vehicle will be placed floating. The placement status will not be updated
        """
        self._vehicle.place_vehicle(self._old_base_point, self._old_rotation, floating=True)
        self.aborted.emit()


    def deactivate(self):
        self._click_counter = 0  # Set click counter to always start with positioning
        self._canvas.scene().removeItem(self._marker)  # Remove the rubber band

from qgis.gui import QgsMapToolEmitPoint, QgisInterface, QgsMapCanvas, QgsMapMouseEvent


class VehiclePlacer(QgsMapToolEmitPoint):
    def __init__(self, iface: QgisInterface):
        self.iface: QgisInterface = iface
        self.canvas: QgsMapCanvas = iface.mapCanvas()
        QgsMapToolEmitPoint.__init__(self, self.canvas)

    def canvasPressEvent(self, e: QgsMapMouseEvent):
        self._clicked_point = self.toMapCoordinates(e.pos())

    @property
    def clicked_point(self):
        return self._clicked_point
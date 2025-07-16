# Simulator class
from qgis.PyQt.QtCore import QObject, pyqtSignal, QTimer
from qgis.gui import QgisInterface, QgsMapCanvas

from .vehicle import Vehicle


class Simulator(QObject):
    # Signals
    steeringChanged = pyqtSignal(float, name="steeringChanged")
    speedChanged = pyqtSignal(float, name="speedChanged")

    def __init__(self, iface: QgisInterface, vehicle: Vehicle):
        super().__init__(self)

        self._iface: QgisInterface = iface
        self._canvas: QgsMapCanvas = iface.mapCanvas()
        self._vehicle: Vehicle = vehicle

        self._simulation_running: bool = False
        self._simulation_timer = QTimer(self)
        self._simulation_timer.timeout.connect(self._simulate)


    def startSimulation(self):
        self._simulation_running = True
        self._simulation_timer.start(40)

    def stopSimulation(self):
        self._simulation_timer.stop()
        self._simulation_running = False

    def speedUp(self):
        if self._simulation_running:
            self._vehicle.speed_up()
            self.speedChanged.emit(self._vehicle.speed)

    def speedDown(self):
        if self._simulation_running:
            self._vehicle.speed_down()
            self.speedChanged.emit(self._vehicle.speed)

    def steerRight(self):
        if self._simulation_running:
            self._vehicle.steer_right()
            self.steeringChanged.emit(self._vehicle.steering_angle)

    def steerLeft(self):
        if self._simulation_running:
            self._vehicle.steer_left()
            self.steeringChanged.emit(self._vehicle.steering_angle)

    def _simulate(self):
        if self._vehicle.speed > 0.05:
            self._vehicle.step()

            if not self.canvas.isDrawing():
                self._draw_vehicle()
            time.sleep(self.vehicle.simulation_step / self.vehicle.speed)

            if self._print_path:
                self._store_path_points()
        else:
            pass

    def setVehicle(self, vehicle: Vehicle):
        """Set vehicle for simulation"""
        self._vehicle = vehicle


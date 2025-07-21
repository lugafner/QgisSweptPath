# Simulator class
import time

from enum import Enum
from threading import Thread
from typing import override

from qgis.PyQt.QtCore import QObject, pyqtSignal, QTimer, QEvent, Qt
from qgis.PyQt.QtGui import QKeySequence
from qgis.core import Qgis
from qgis.gui import QgsMapTool

from .qgis_swept_path_dockwidget_prop import QgisSweptPathDockWidgetProp
from .vehicle import Vehicle
from .qgis_swept_path_enum import SimulationMode


class Simulator(QgsMapTool):
    # Signals
    drawVehicle: pyqtSignal = pyqtSignal(name="drawVehicle")
    storePath: pyqtSignal = pyqtSignal(name="storePath")

    def __init__(self, iface):
        """Constructor"""
        QgsMapTool.__init__(self, iface.mapCanvas())

        self._vehicle: Vehicle = None
        self._prop: QgisSweptPathDockWidgetProp = None

        self._simulation_running: bool = False
        self._simulation_timer: QTimer = QTimer(self)
        self._simulation_timer.timeout.connect(self._simulate_frame)

        # Number of frames to steer from center to full steering angle
        self._frames_half_steering: float = None
        # Time between steps in milliseconds
        self._time_between_steps: int = None

        # Flags for steering and speed change
        self._steer_right: bool = False
        self._steer_left: bool = False
        self._speed_up: bool = False
        self._speed_down: bool = False


    def keyPressEvent(self, event):
        if event.key() == QKeySequence(self._prop.key_steer_left):
            self._steer_left = True
        if event.key() == QKeySequence(self._prop.key_steer_right):
            self._steer_right = True
        if event.key() == QKeySequence(self._prop.key_speed_up):
            self._speed_up = True
        if event.key() == QKeySequence(self._prop.key_speed_down):
            self._speed_down = True


    def keyReleaseEvent(self, event):
        if event.key() == QKeySequence(self._prop.key_steer_left):
            self._steer_left = False
        if event.key() == QKeySequence(self._prop.key_steer_right):
            self._steer_right = False
        if event.key() == QKeySequence(self._prop.key_speed_up):
            self._speed_up = False
        if event.key() == QKeySequence(self._prop.key_speed_down):
            self._speed_down = False


    def startSimulation(self):
        self._simulation_running = True
        if self._prop.simulation_mode == SimulationMode.FRAME_BASED:
            self._frames_half_steering = self._prop.steering_speed / 2 * self._prop.frames
            self._time_between_steps = int(1000 / self._prop.frames)
            self._simulation_timer.start(self._time_between_steps)

        elif self._prop.simulation_mode == SimulationMode.STEP_BASED:
            t = Thread(target=self._simulate_step, args=())
            t.start()
            
        else:
            self.iface.messageBar().pushMessage(
                "Can't start simulation",
                "Unknown simulation mode",
                level=Qgis.Critical
            )


    def stopSimulation(self):
        self._simulation_running = False
        if self._prop.simulation_mode == SimulationMode.FRAME_BASED:
            self._simulation_timer.stop()

        self.drawVehicle.emit()
        # self.storePath.emit()


    def speedUp(self):
        if not self._speed_down:
            self._speed_up = True
        self._speed_down = False


    def speedDown(self):
        if not self._speed_up:
            self._speed_down = True
        self._speed_up = False


    def steerRight(self):
        if not self._steer_left:
            self._steer_right = True
        self._steer_left = False


    def steerLeft(self):
        if not self._steer_right:
            self._steer_left = True
        self._steer_right = False


    def _simulate_frame(self):
        if self._speed_up:
            self._vehicle.speed_up(self._prop.speed_change_step)

        if self._speed_down:
            self._vehicle.speed_down(self._prop.speed_change_step)

        if self._steer_right:
            self._vehicle.steer_right(self._vehicle.max_steering_angle / self._frames_half_steering)

        if self._steer_left:
            self._vehicle.steer_left(self._vehicle.max_steering_angle / self._frames_half_steering)

        if self._vehicle.speed > self._prop.minimum_speed:
            self._vehicle.step(float(self._time_between_steps) / 1000.0 * self._vehicle.speed)

        self.drawVehicle.emit()

        # TODO check if must store (draw vehicle property and steps/distance)
        # self.storePath.emit()


    def _simulate_step(self):
        while self._simulation_running:
            if self._speed_up:
                self._vehicle.speed_up(self._prop.speed_change_step)

            if self._speed_down:
                self._vehicle.speed_down(self._prop.speed_change_step)

            if self._steer_right:
                self._vehicle.steer_right(self._vehicle.max_steering_angle / self._frames_half_steering)

            if self._steer_left:
                self._vehicle.steer_left(self._vehicle.max_steering_angle / self._frames_half_steering)

            if self._vehicle.speed > self._prop.minimum_speed:
                self._vehicle.step(self._prop.step_distance)

            self.drawVehicle.emit()

            # TODO check if must store (draw vehicle property and steps/distance)
            # self.storePath.emit()

            time.sleep(self.vehicle.simulation_step / self.vehicle.speed)


    @property
    def simulation_running(self) -> bool:
        return self._simulation_running


    @property
    def properties(self) -> QgisSweptPathDockWidgetProp:
        return self._prop


    @properties.setter
    def properties(self, v: QgisSweptPathDockWidgetProp):
        self._prop = v


    @property
    def vehicle(self) -> Vehicle:
        return self._vehicle


    @vehicle.setter
    def vehicle(self, v: Vehicle):
        self._vehicle = v

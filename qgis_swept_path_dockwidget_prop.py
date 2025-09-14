import math
import os
from typing import override

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QDockWidget, QFileDialog
from qgis.core import QgsProject

from .qgis_swept_path_enum import SimulationMode, BorderDistanceUnits


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'qgis_swept_path_dockwidget_prop.ui'))

class QgisSweptPathDockWidgetProp(QDockWidget, FORM_CLASS):
    # Signals
    vehicleLayerChanged: pyqtSignal = pyqtSignal(name="VehicleLayerChanged")
    pathLayerChanged: pyqtSignal = pyqtSignal(name="PathLayerChanged")

    def __init__(self, parent=None):
        """Constructor."""
        super(QgisSweptPathDockWidgetProp, self).__init__(parent)
        self.setupUi(self)
        self.proj: QgsProject = QgsProject.instance()

        # Properties with default values
        self._frames: int = 24  # Frames per second for frame based simulation
        self._step_distance: float = 0.05  # Distance for step based simulation
        self._print_path: bool = True  # Do or do not print path
        self._print_interval: int = 2  # Interval storing path points for step based simulation
        self._print_distance: float = 1.00  # Distance between storing path points for frame based simulation.
        self._vehicle_layer_style: str = "./style/vehicle.qml"  # Path to qgis layer style for vehicle layer. Absolute or relative to the plugin dir.
        self._path_layer_style: str = "./style/path.qml"  # Path to qgis layer style for path layer. Absolute or relative to the plugin dir.
        self._vehicle_layer_id: str = ""  # Layer id of vehicle layer
        self._path_layer_id: str = ""  # Layer id of path layer
        self._dissolve_path: bool = False  # Do or do not dissolve the paths
        self._dissolve_fields: str = ""  # String of fields to dissolve the paths by (semicolon separated)
        self._speed_change_step: float = 0.05  # Steps to change speed in m/s per click (step based)
        self._steer_change_step: float = 0.008  # Radians per click (step based)
        self._steering_time: float = 6.0  # Time in seconds for full left to full right (frame based)
        self._acceleration: float = 2.5  # Acceleration and deceleration in m/s2 (frame based)
        self._minimum_speed: float = 0.01  # Minimum speed before the vehicle stops
        self._simulation_mode: int = SimulationMode.FRAME_BASED.value  # Integer representation of simulation mode enum
        self._key_steer_left: str = "J"  # Single key for steering left
        self._key_steer_right: str = "L"  # Single key for steering right
        self._key_speed_up: str = "I"  # Single key for speed up
        self._key_speed_down: str = "K"  # Single key for speed down
        self._vehicle_packages: str = ""  # String of additional directories with vehicle packages (semicolon separated)
        self._border_distance_units: int = BorderDistanceUnits.MAP_UNITS.value  # Integer representation of distance units
        self._auto_map_movement: bool = True  # Automatic map movement
        self._border_distance: float = 10.0  # Minimal distance from border for automatic map movement (Units see above)


        # Dict with all property fields registered (k = field name, v = qgis property path)
        self._properties: dict[str, str] = {
            "_frames": "frames",
            "_step_distance": "step_distance",
            "_print_path": "print_path",
            "_print_interval": "print_interval",
            "_print_distance": "print_distance",
            "_vehicle_layer_style": "vehicle_layer_style",
            "_path_layer_style": "path_layer_style",
            "_vehicle_layer_id": "vehicle_layer_id",
            "_path_layer_id": "path_layer_id",
            "_dissolve_path": "dissolve_path",
            "_dissolve_fields": "dissolve_fields",
            "_speed_change_step": "speed_change_step",
            "_steer_change_step": "steer_change_step",
            "_steering_time": "steering_time",
            "_acceleration": "acceleration",
            "_minimum_speed": "minimum_speed",
            "_simulation_mode": "simulation_mode",
            "_key_steer_left": "key_steer_left",
            "_key_steer_right": "key_steer_right",
            "_key_speed_up": "key_speed_up",
            "_key_speed_down": "key_speed_down",
            "_vehicle_packages": "vehicle_packages",
            "_border_distance_units": "border_distance_units",
            "_auto_map_movement": "auto_map_movement",
            "_border_distance": "border_distance"
        }

        # Fields to store the information, if the layer ids were changed
        # If the layer ids were changed, the signals are emitted on close
        self._vehicle_layer_changed: bool = False
        self._path_layer_changed: bool = False

        self._readProperties()  # Read the properties from QGIS project
        self._initGUI()  # Sets up slots


    @override
    def closeEvent(self, event):
        self._write_properties()

        # Check if the layers are changed and emit the signal
        if self._vehicle_layer_changed:
            self._vehicle_layer_changed = False
            self.vehicleLayerChanged.emit()
        if self._path_layer_changed:
            self._path_layer_changed = False
            self.pathLayerChanged.emit()

        event.accept()


    @override
    def showEvent(self, event):
        self._updateGUI()  # Fills the GUI objects with the values
        event.accept()


    def _initGUI(self):
        """
        Set up signals for property changes
        """
        self.propPrintPath.stateChanged.connect(self._change_print_path)
        self.btnVehicleLayerStyle.clicked.connect(self._change_vehicle_layer_style)
        self.btnPathLayerStyle.clicked.connect(self._change_path_layer_style)
        self.propFrames.valueChanged.connect(self._change_frames)
        self.propStepDistance.valueChanged.connect(self._change_step_distance)
        self.propDissolvePath.stateChanged.connect(self._change_dissolve_path)
        self.propDissolveFields.textEdited.connect(self._change_dissolve_fields)
        self.propPrintInterval.valueChanged.connect(self._change_print_interval)
        self.propPrintDistance.valueChanged.connect(self._change_print_distance)
        self.propSpeedChangeStep.valueChanged.connect(self._change_speed_change_step)
        self.propSteerChangeStep.valueChanged.connect(self._change_steer_change_step)
        self.propSteeringTime.valueChanged.connect(self._change_steering_time)
        self.propAcceleration.valueChanged.connect(self._change_acceleration)
        self.propMinimumSpeed.valueChanged.connect(self._change_minimum_speed)
        self.propKeySteerLeft.textEdited.connect(self._change_key_steer_left)
        self.propKeySteerRight.textEdited.connect(self._change_key_steer_right)
        self.propKeySpeedUp.textEdited.connect(self._change_key_speed_up)
        self.propKeySpeedDown.textEdited.connect(self._change_key_speed_down)
        self.propFrameBasedSimulation.clicked.connect(self._clicked_frame_based_simulation)
        self.propStepBasedSimulation.clicked.connect(self._clicked_step_based_simulation)
        self.propVehiclePackages.textEdited.connect(self._change_vehicle_packages)
        self.propVehicleLayerId.textEdited.connect(self._change_vehicle_layer_id)
        self.propPathLayerId.textEdited.connect(self._change_path_layer_id)
        self.propBorderDistance.valueChanged.connect(self._change_border_distance)
        self.propAutoMapMovement.stateChanged.connect(self._change_auto_map_movement)
        self.propDistanceMapUnits.clicked.connect(self._clicked_distance_map_units)
        self.propDistancePixels.clicked.connect(self._clicked_distance_pixels)

        # Layer id editing check boxes (no properties to be saved)
        self.chbEditVehicleLayer.clicked.connect(self._clicked_edit_vehicle_layer)
        self.chbEditPathLayer.clicked.connect(self._clicked_edit_path_layer)


    def _updateGUI(self):
        """
        Fills the property values in the gui objects
        """
        self.propVehicleLayerId.setText(self._vehicle_layer_id)
        self.propPathLayerId.setText(self._path_layer_id)
        self.propPrintPath.setChecked(self._print_path)
        self.propVehicleLayerStyle.setText(self._vehicle_layer_style)
        self.propPathLayerStyle.setText(self._path_layer_style)
        self.propFrames.setValue(self._frames)
        self.propStepDistance.setValue(self._step_distance)
        self.propDissolvePath.setChecked(self._dissolve_path)
        self.propDissolveFields.setText(self._dissolve_fields)
        self.propPrintInterval.setValue(self._print_interval)
        self.propPrintDistance.setValue(self._print_distance)
        self.propSpeedChangeStep.setValue(self._speed_change_step)
        self.propSteerChangeStep.setValue(self._steer_change_step * 180.0 / math.pi)
        self.propSteeringTime.setValue(self._steering_time)
        self.propAcceleration.setValue(self._acceleration)
        self.propMinimumSpeed.setValue(self._minimum_speed)
        self.propKeySteerLeft.setText(self._key_steer_left)
        self.propKeySteerRight.setText(self._key_steer_right)
        self.propKeySpeedUp.setText(self._key_speed_up)
        self.propKeySpeedDown.setText(self._key_speed_down)
        self.propVehiclePackages.setText(self._vehicle_packages)
        self.propBorderDistance.setValue(self._border_distance)
        self.propAutoMapMovement.setChecked(self._auto_map_movement)

        if self._simulation_mode == SimulationMode.FRAME_BASED:
            self.propStepBasedSimulation.setChecked(False)
            self.propFrameBasedSimulation.setChecked(True)
        elif self._simulation_mode == SimulationMode.STEP_BASED:
            self.propFrameBasedSimulation.setChecked(False)
            self.propStepBasedSimulation.setChecked(True)
        else:
            raise Exception("Unknown property for simulation mode")

        if self._border_distance_units == BorderDistanceUnits.MAP_UNITS:
            self.propDistancePixels.setChecked(False)
            self.propDistanceMapUnits.setChecked(True)
        elif self._border_distance_units == BorderDistanceUnits.PIXELS:
            self.propDistanceMapUnits.setChecked(False)
            self.propDistancePixels.setChecked(True)
        else:
            raise Exception("Unknown property for border distance units")


    def _readProperties(self):
        """
        Read properties from QGIS project
        and load into the fields
        """
        for k, v in self._properties.items():
            default_value = getattr(self, k)
            if isinstance(default_value, str):
                read_function = self.proj.readEntry
            elif isinstance(default_value, int):
                read_function = self.proj.readNumEntry
            elif isinstance(default_value, float):
                read_function = self.proj.readDoubleEntry
            elif isinstance(default_value, bool):
                read_function = self.proj.readBoolEntry
            else:
                continue

            attr , type_conversion_ok = read_function("QgisSweptPath", v, getattr(self, k))
            if type_conversion_ok:
                setattr(self, k, attr)


    def _write_properties(self):
        """
        Writes the properties to the QGIS project
        """
        for k, v in self._properties.items():
            current_value = getattr(self, k)
            if isinstance(current_value, str):
                write_function = self.proj.writeEntry
            elif isinstance(current_value, int):
                write_function = self.proj.writeEntry
            elif isinstance(current_value, float):
                write_function = self.proj.writeEntryDouble
            elif isinstance(current_value, bool):
                write_function = self.proj.writeEntryBool
            else:
                continue

            write_function("QgisSweptPath", v, getattr(self, k))


    def _show_file_select_dialog(self,
                                 title: str = "Open file",
                                 file_types: list[str] = ["Any files (*)"]) -> str | None:
        """
        Shows an open file dialog for a single file
        @param title: String for title of the dialog
        @param file_types: String list of file type filter
        @return: Absolute file path as string or None if no file is selected
        """
        dialog = QFileDialog(self)
        dialog.setWindowTitle(title)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilters(file_types)

        if dialog.exec():
            return dialog.selectedFiles()[0]
        else:
            return None


    def _change_print_path(self):
        self._print_path = bool(self.propPrintPath.isChecked())


    def _change_vehicle_layer_style(self):
        file_filter = [
            "QGIS layer style (*.qml)",
            "Any files (*)"
        ]
        style_file = self._show_file_select_dialog("Open vehicle layer style", file_filter)
        if style_file:
            self._vehicle_layer_style = style_file
            self.propVehicleLayerStyle.setText(style_file)
        else:
            pass


    def _change_path_layer_style(self):
        file_filter = [
            "QGIS layer style (*.qml)",
            "Any files (*)"
        ]
        style_file = self._show_file_select_dialog("Open path layer style", file_filter)
        if style_file:
            self._path_layer_style = style_file
            self.propPathLayerStyle.setText(style_file)
        else:
            pass

    def _change_frames(self):
        self._frames = int(self.propFrames.value())


    def _change_step_distance(self):
        self._step_distance = float(self.propStepDistance.value())


    def _change_dissolve_path(self):
        self._dissolve_path = bool(self.propDissolvePath.isChecked())


    def _change_dissolve_fields(self):
        self._dissolve_fields = str(self.propDissolveFields.text())


    def _change_print_interval(self):
        self._print_interval = int(self.propPrintInterval.value())


    def _change_print_distance(self):
        self._print_distance = float(self.propPrintDistance.value())


    def _change_speed_change_step(self):
        self._speed_change_step = float(self.propSpeedChangeStep.value())


    def _change_steer_change_step(self):
        self._steer_change_step = float(self.propSteerChangeStep.value() * math.pi / 180.0)


    def _change_minimum_speed(self):
        self._minimum_speed = float(self.propMinimumSpeed.value())


    def _change_steering_time(self):
        self._steering_time = float(self.propSteeringTime.value())


    def _change_acceleration(self):
        self._acceleration = float(self.propAcceleration.value())


    def _change_key_steer_left(self):
        self._key_steer_left = str(self.propKeySteerLeft.text())


    def _change_key_steer_right(self):
        self._key_steer_right = str(self.propKeySteerRight.text())


    def _change_key_speed_up(self):
        self._key_speed_up = str(self.propKeySpeedUp.text())


    def _change_key_speed_down(self):
        self._key_speed_down = str(self.propKeySpeedDown.text())


    def _clicked_frame_based_simulation(self):
        self.propStepBasedSimulation.setChecked(False)
        self._simulation_mode = int(SimulationMode.FRAME_BASED.value)


    def _clicked_step_based_simulation(self):
        self.propFrameBasedSimulation.setChecked(False)
        self._simulation_mode = int(SimulationMode.STEP_BASED.value)


    def _change_vehicle_packages(self):
        self._vehicle_packages = str(self.propVehiclePackages.text())


    def _change_path_layer_id(self):
        self._path_layer_id = str(self.propPathLayerId.text())


    def _change_vehicle_layer_id(self):
        self._vehicle_layer_id = str(self.propVehicleLayerId.text())


    def _change_border_distance(self):
        self._border_distance = float(self.propBorderDistance.value())


    def _change_auto_map_movement(self):
        self._auto_map_movement = bool(self.propAutoMapMovement.isChecked())


    def _clicked_distance_map_units(self):
        self.propDistancePixels.setChecked(False)
        self._border_distance_units = int(BorderDistanceUnits.MAP_UNITS.value)


    def _clicked_distance_pixels(self):
        self.propDistanceMapUnits.setChecked(False)
        self._border_distance_units = int(BorderDistanceUnits.PIXELS.value)


    def _clicked_edit_path_layer(self):
        self._path_layer_changed = True
        if self.chbEditPathLayer.isChecked():
            self.propPathLayerId.setReadOnly(True)
        else:
            self.propPathLayerId.setReadOnly(False)


    def _clicked_edit_vehicle_layer(self):
        self._vehicle_layer_changed = True
        if self.chbEditVehicleLayer.isChecked():
            self.propVehicleLayerId.setReadOnly(True)
        else:
            self.propVehicleLayerId.setReadOnly(False)


    @property
    def frames(self) -> int:
        """Frames per seconds for simulation"""
        return self._frames


    @property
    def step_distance(self) -> float:
        """Distance for step based simulation"""
        return self._step_distance


    @property
    def vehicle_layer_style(self) -> str:
        """
        Path to qgis layer style for vehicle layer.
        Absolute or relative to the plugin directory
        """
        return self._vehicle_layer_style


    @property
    def path_layer_style(self) -> str:
        """
        Path to qgis layer style for path layer.
        Absolute or relative to the plugin directory
        """
        return self._path_layer_style


    @property
    def vehicle_layer_id(self) -> str:
        """Layer id of vehicle layer"""
        return self._vehicle_layer_id


    @property
    def path_layer_id(self) -> str:
        """Layer id of path layer"""
        return self._path_layer_id


    @property
    def print_path(self) -> bool:
        """Do or do not print path"""
        return self._print_path


    @property
    def dissolve_path(self) -> bool:
        """Do or do not dissolve the paths"""
        return self._dissolve_path


    @property
    def dissolve_fields(self) -> str:
        """
        String of fields to dissolve the paths by
        Semicolon separated
        """
        return self._dissolve_fields


    @property
    def print_interval(self) -> int:
        """Interval storing path points for step based simulation"""
        return self._print_interval


    @property
    def print_distance(self):
        """Distance between storing path points for frame based simulation"""
        return self._print_distance


    @property
    def steering_time(self) -> float:
        """Steering time in seconds from full left to full right"""
        return self._steering_time


    @property
    def acceleration(self) -> float:
        """Acceleration or deceleration in m/s2"""
        return self._acceleration


    @property
    def speed_change_step(self) -> float:
        """Step to change speed in step based mode"""
        return self._speed_change_step


    @property
    def steer_change_step(self) -> float:
        """Step to change steering in step based mode"""
        return self._steer_change_step


    @property
    def minimum_speed(self) -> float:
        """Minimum speed before vehicle stops in m/s"""
        return self._minimum_speed


    @property
    def simulation_mode(self) -> SimulationMode:
        """Simulation mode"""
        return self._simulation_mode


    @property
    def key_speed_up(self) -> str:
        """Key speed up as string"""
        return self._key_speed_up


    @property
    def key_speed_down(self) -> str:
        """Key speed down as string"""
        return self._key_speed_down


    @property
    def key_steer_left(self) -> str:
        """Key steer left as string"""
        return self._key_steer_left


    @property
    def key_steer_right(self) -> str:
        """Key steer right as string"""
        return self._key_steer_right


    @property
    def vehicle_packages(self) -> str:
        """Semicolon separated string of vehicle package directories"""
        return self._vehicle_packages


    @property
    def border_distance_units(self) -> BorderDistanceUnits:
        """Border Distance Units"""
        return self._border_distance_units


    @property
    def auto_map_movement(self) -> bool:
        """True if the automatic map movement is on"""
        return self._auto_map_movement


    @property
    def border_distance(self) -> float:
        """Minimal distance from border for automatic map movement"""
        return self._border_distance


    # Setters
    # The write properties must be called after each value change from outside the GUI
    def set_path_layer_id(self, v: str):
        """Set the layer id of path layer"""
        self._path_layer_id = v
        self._write_properties()


    def set_vehicle_layer_id(self, v: str):
        """Set the layer id of vehicle layer"""
        self._vehicle_layer_id = v
        self._write_properties()

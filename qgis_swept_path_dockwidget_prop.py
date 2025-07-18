
import os
from typing import override, Any

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDockWidget, QFileDialog
from qgis.core import QgsSettings


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'qgis_swept_path_dockwidget_prop.ui'))

class QgisSweptPathDockWidgetProp(QDockWidget, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(QgisSweptPathDockWidgetProp, self).__init__(parent)
        self.setupUi(self)

        # Properties with default values
        self._frames: int = 24  # Frames per second for frame based simulation. TODO: Implement frame based simulation
        self._step_distance: float = 0.05  # Distance for step based simulation
        self._print_path: bool = True  # Do or do not print path
        self._print_interval: int = 2  # Interval storing path points for step based simulation TODO: Implement frame based simulation
        self._print_distance: float = 1.00  # Distance between storing path points for frame based simulation.
        self._vehicle_layer_style: str = "./style/vehicle.qml"  # Path to qgis layer style for vehicle layer. Absolute or relative to the plugin dir.
        self._path_layer_style: str = "./style/path.qml"  # Path to qgis layer style for path layer. Absolute or relative to the plugin dir.
        self._vehicle_layer_id: str = ""  # Layer id of vehicle layer
        self._path_layer_id: str = ""  # Layer id of path layer
        self._dissolve_path: bool = False  # Do or do not dissolve the paths
        self._dissolve_fields: str = ""  # String of fields to dissolve the paths by (comma separated)

        # Dict with all property fields registered (k = field name, v = qgis property path)
        self._properties: dict[str, str] = {
            "_frames": "qgissweptpath/frames",
            "_step_distance": "qgissweptpath/step_distance",
            "_print_path": "qgissweptpath/print_path",
            "_print_interval": "qgissweptpath/print_interval",
            "_print_distance": "qgissweptpath/print_distance",
            "_vehicle_layer_style": "qgissweptpath/vehicle_layer_style",
            "_path_layer_style": "qgissweptpath/path_layer_style",
            "_vehicle_layer_id": "qgissweptpath/vehicle_layer_id",
            "_path_layer_id": "qgissweptpath/path_layer_id",
            "_dissolve_path": "qgissweptpath/dissolve_path",
            "_dissolve_fields": "qgissweptpath/dissolve_fields"
        }

        self._readProperties()  # Read the properties from QGIS project
        self._initGUI()  # Sets up slots


    @override
    def closeEvent(self, event):
        self._write_properties()
        event.accept()


    @override
    def showEvent(self, event):
        self._updateGUI()  # Fills the GUI objects with the values
        event.accept()


    def _initGUI(self):
        """
        Set up slots for property changes
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


    def _readProperties(self):
        """
        Read properties from QGIS project
        and load into the fields
        """
        settings = QgsSettings()
        for k, v in self._properties.items():
            setattr(self, k, settings.value(v, getattr(self, k), type=type(getattr(self, k))))


    def _write_properties(self):
        """
        Writes the properties to the QGIS project
        """
        settings = QgsSettings()
        for k, v in self._properties.items():
            settings.setValue(v, getattr(self, k))


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
        Comma separated
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


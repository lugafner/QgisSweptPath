
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
        self._frames: int = 24  # Frames per seconds for simulation. TODO: Implementation for frame based simulation
        self._step_distance: float = 0.05  # Distance for step based simulation
        self._print_path: bool = True  # Do or do not print path
        self._vehicle_layer_style: str = ""  # Path to qgis layer style for vehicle layer
        self._path_layer_style: str = ""  # Path to qgis layer style for path layer
        self._vehicle_layer: str = ""  # Layer id of vehicle layer
        self._path_layer: str = ""  # Layer id of path layer
        self._dissolve_path: bool = False  # Do or do not dissolve the paths
        self._dissolve_fields: str = ""  # List of fields to dissolve the paths by

        # Dict with all property fields registered (k = field name, v = qgis property path)
        self._properties: dict[str, str] = {
            "_frames": "qgissweptpath/frames",
            "_step_distance": "qgissweptpath/step_distance",
            "_print_path": "qgissweptpath/print_path",
            "_vehicle_layer_style": "qgissweptpath/vehicle_layer_style",
            "_path_layer_style": "qgissweptpath/path_layer_style",
            "_vehicle_layer": "qgissweptpath/vehicle_layer",
            "_path_layer": "qgissweptpath/path_layer",
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
        self.propDissolvePath.stateChanged.connect(self._change_dissolve_path)
        self.propDissolveFields.textEdited.connect(self._change_dissolve_fields)



    def _updateGUI(self):
        """
        Fills the property values in the gui objects
        """
        self.propVehicleLayer.setText(self._vehicle_layer)
        self.propPathLayer.setText(self._path_layer)
        self.propPrintPath.setChecked(self._print_path)
        self.propVehicleLayerStyle.setText(self._vehicle_layer_style)
        self.propPathLayerStyle.setText(self._path_layer_style)
        self.propFrames.setValue(self._frames)
        self.propStepDistance.setValue(self._step_distance)
        self.propDissolvePath.setChecked(self._dissolve_path)
        self.propDissolveFields.setText(self._dissolve_fields)


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


    def _show_file_select_dialog(self, title: str = "Open file", file_types: list[str] = ["Any files (*)"]):
        dialog = QFileDialog(self)
        dialog.setWindowTitle(title)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilters(file_types)

        if dialog.exec():
            return dialog.selectedFiles()[0]
        else:
            return None


    def _change_print_path(self):
        self._print_path = self.propPrintPath.isChecked()


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


    def _change_dissolve_path(self):
        self._dissolve_path = self.propDissolvePath.isChecked()


    def _change_dissolve_fields(self):
        print(self.propDissolveFields.text)
        self._dissolve_fields = self.propDissolveFields.text()


    @property
    def frames(self) -> int:
        """Simulation frames per seconds"""
        return self._frames

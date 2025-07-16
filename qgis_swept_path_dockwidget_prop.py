
import os
from qgis.PyQt import uic, QtWidgets


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'qgis_swept_path_dockwidget_prop.ui'))

class QgisSweptPathDockWidgetProp(QtWidgets.QDockWidget, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(QgisSweptPathDockWidgetProp, self).__init__(parent)
        self.setupUi(self)

    def closeEvent(self, event):
        # TODO: Store properties in Qgis project
        event.accept()

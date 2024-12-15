from qgis.PyQt.QtCore import QObject, QEvent, Qt

class Controls(QObject):
    def __init__(self, app, parent=None):
       super(Controls, self).__init__(parent)
       self._app = app

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyRelease:
            print("pressed")
            if event.key() == Qt.Key_Up:
                self._app.speed_up()
                print("up")
                return True
            if event.key() == Qt.Key_Down:
                self._app.speed_down()
                return True
            if event.key() == Qt.Key_Left:
                self._app.steer_left()
                return True
            if event.key() == Qt.Key_Right:
                self._app.steer_right()
                return True
        return False


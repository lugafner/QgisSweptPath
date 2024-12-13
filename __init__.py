
def classFactory(iface):
    from .qgis_swept_path import QgisSweptPath
    return QgisSweptPath(iface)

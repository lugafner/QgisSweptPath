from qgis.core import QgsPointXY

from .coord import CartesianCoord


class PathPoints:
    """
    Class to store the path points during simulation
    """

    def __init__(self,
                 vehicle_name: str,
                 vehicle_type: str,
                 vehicle_part_type: str,
                 vehicle_part: str):
        """
        Init a new path point
        @param vehicle_name: Vehicle name (from vehicle class)
        @param vehicle_type: Type main or trailer
        @param vehicle_part_type: Part type wheels or body
        @param vehicle_part: Point name of the vehicle i.e. fwl, fl, br
        """
        self._points: list[CartesianCoord] = []  # List of the points
        self._vehicle_name: str = vehicle_name  # Vehicle name (from vehicle class)
        self._vehicle_type: str = vehicle_type  # Type main or trailer
        self._vehicle_part_type: str = vehicle_part_type  # Part type wheels or body
        self._vehicle_part: str = vehicle_part  # Point name of the vehicle i.e. fwl, fl, br

    def add_point(self, point: CartesianCoord):
        """
        Append a new point to the point list
        @param point: Point to add as CartesianCoord
        """
        self._points.append(point)

    def get_list_as_cartesian(self) -> list[CartesianCoord]:
        """ Returns the points as CartesionCoords in a one dimensional list """
        return self._points

    def get_list_as_qgs_points(self) -> list[QgsPointXY]:
        """ Returns the point list as QgsPointXY """
        point_list = []
        for p in self._points:
            point_list.append(QgsPointXY(p.x, p.y))

        return point_list

    @property
    def vehicle_name(self) -> str:
        """ Returns vehicle name (from vehicle class) """
        return self._vehicle_name

    @property
    def vehicle_type(self) -> str:
        """ Returns type main or trailer """
        return self._vehicle_type

    @property
    def vehicle_part_type(self) -> str:
        """ Returns part type wheels or body """
        return  self._vehicle_part_type

    @property
    def vehicle_part(self) -> str:
        """ Returns point name of the vehicle i.e. fwl, fl, br """
        return self._vehicle_part


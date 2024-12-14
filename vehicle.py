import math

from typing import Final
from coord import PolarCoord, CartesianCoord, CoordUtils


class Vehicle:
    def __init__(self):
        # Vehicle input parameters (TODO: Constructor parameters)
        # Body
        self._body_length: Final[float] = 15.00  # meter
        self._body_width: Final[float] = 2.50  # meter
        # Chassis
        self._front_axle_ref_pos: Final[float] = 3.10  # meter from front
        self._rear_axle_ref_pos: Final[float] = 11.65  # meter from front
        self._axle_with: Final[float] = 2.50  # meter
        # Steering
        self._max_steering_angle: Final[float] = 53.0 / 180 * 3.14159  # radian
        # Trailer
        self._trailer: Final[Vehicle] = None
        # Connection point must always be initialised with a value
        self._connection_point: Final[float] = 11.65

        # Vehicle local crs (polar from F)
        #   BL     RWL             FWL   FL
        #   +------+---------------+-----+
        #   |                            |
        #   CP - - H - - - - - - - F - - +  Front (x direction)
        #   |                            |
        #   +------+---------------+-----+
        #   BR     RWR             FWR   FR
        # Calculated parameters
        self._wheelbase: Final[float] = self._rear_axle_ref_pos - self._front_axle_ref_pos
        back_distanz: Final[float] = self._body_length - self._front_axle_ref_pos
        connection_point_distance: Final[float] = self._connection_point - self._front_axle_ref_pos
        wheel_side_offset: Final[float] = self._axle_with / 2
        body_side_offset: Final[float] = self._body_width / 2

        self._local_point_h: Final[PolarCoord] = CoordUtils.toPolar(- self._wheelbase, 0.0)
        self._local_point_bl: Final[PolarCoord] = CoordUtils.toPolar(- back_distanz, body_side_offset)
        self._local_point_rwl: Final[PolarCoord] = CoordUtils.toPolar(- self._wheelbase, wheel_side_offset)
        self._local_point_fwl: Final[PolarCoord] = CoordUtils.toPolar(0.0, wheel_side_offset)
        self._local_point_fl: Final[PolarCoord] = CoordUtils.toPolar(self._front_axle_ref_pos, body_side_offset)
        self._local_point_br: Final[PolarCoord] = CoordUtils.toPolar(- back_distanz, - body_side_offset)
        self._local_point_rwr: Final[PolarCoord] = CoordUtils.toPolar(- self._wheelbase, - wheel_side_offset)
        self._local_point_fwr: Final[PolarCoord] = CoordUtils.toPolar(0.0, - wheel_side_offset)
        self._local_point_fr: Final[PolarCoord] = CoordUtils.toPolar(self._front_axle_ref_pos, - wheel_side_offset)
        self._local_point_cp: Final[PolarCoord] = CoordUtils.toPolar(- connection_point_distance, 0.0)

        # Initialise Fehicle position
        self._global_f = CartesianCoord(0.0, 0.0)  # Initialize reference point with 0, 0
        self._global_h = CartesianCoord(- self._wheelbase, 0.0)
        self._global_a: float = self._calc_azimuth()  # Initialize azimuth (get from f and h)
        self._global_cp: CartesianCoord = self._calc_global_coord(self._local_point_cp)
        

    def _calc_azimuth(self) -> float:
        """Calculates the azimut of the vehicle based on the points f and h

        @return: Azimut of the vehicle (0.0 = facing east)
        """
        dx = self._global_f.x - self._global_h.x
        dy = self._global_f.y - self._global_h.y
        return math.atan2(dy, dx)

    def _calc_global_coord(self, local_coord: PolarCoord) -> CartesianCoord:
        """
        Calculate the global coordinate for a local polar coordinate
        Based on current position and rotation of the vehicle

        @param local_coord: The local coordinate as polar coordinate
        @return: The global coordinate
        """
        new_azimut: float = self._global_a + local_coord.a
        cartesian_shift: CartesianCoord = CoordUtils.toCartesian(local_coord.d, new_azimut)
        return cartesian_shift + self._global_f 

    def place_vehicle(self, f:CartesianCoord, a:float):
        """ 
        Place the vehicle at a given point and calculate the base point h
        This function is only needet at first vehicle placement
        During driving, the azimuth a is not known

        @param f: Coordinate of reference point f
        @param a: Azimuth of the vehicle (0.0 facing east)
        """         
        self._global_f = f
        self._global_a = a
        self._global_h = self._calc_global_coord(self._local_point_h)
        self._global_cp = self._calc_global_coord(self._local_point_cp)

        # Place trailer
        if (self._trailer):
            self._trailer.place_vehicle(self._global_cp, self._global_a)


    def step(self, steering_angle:float, simulation_step:float=0.5):
        """
        Calculates the next point based on current location and steering angle

        @param steering_angle: Steering angle in rad (negative=right, positive=left)
        @param simulation_step: Distance to drive per step (TODO: Calibrate)
        @return: All global vehicle coordinates (TODO: Are they needed?)
        """
        driving_vector = PolarCoord(simulation_step, steering_angle)
        self._global_f = self._calc_global_coord(driving_vector)
        self._global_a = self._calc_azimuth()
        self._global_h = self._calc_global_coord(self._local_point_h)
        self._global_cp = self._calc_global_coord(self._local_point_cp)
        
        # TODO: Call function for the rest of the body points

        # Simulate trailer
        if (self._trailer):
            self._trailer.step_trailer(self._global_cp)

    def step_trailer(self, connection_point:CartesianCoord):
        """
        Simulate the movement of a trailer based on connection point
        The connection point from the parent vehicle ist the reference point f of the trailer
        
        @param connection_point: Global cartesian coordinate of the connection point
        """
        self._global_f = connection_point
        self._global_a = self._calc_azimuth()
        self._global_h = self._calc_global_coord(self._local_point_cp)

        # TODO: Call function for the rest of the body points

        # Simulate trailer
        if (self._trailer):
            self._trailer.step_trailer(self._global_cp)
           
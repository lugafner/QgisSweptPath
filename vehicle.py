import math
import inspect

from pathlib import Path
from typing import Optional

from .coord import PolarCoord, CartesianCoord, CoordUtils


class Vehicle:
    vehicle_name: str = "Vehicle"
    """Name of vehicle. Will be shown in combo box for vehicle selection"""
    is_main_vehicle: bool = False
    """Set as main vehicle or just as trailer part. Only main vehicles are shown for vehicle selection"""


    def __init__(self):
        # **************************************************************************************************************
        # Vehicle input parameters. Setup for new vehicle extending this class
        # Body
        self._body_length: float = 15.00  # meter
        self._body_width: float = 2.50  # meter
        # Chassis
        self._front_axle_ref_pos: float = 3.10  # meter from front
        self._rear_axle_ref_pos: float = 11.65  # meter from front
        self._axle_with: float = 2.50  # meter incl. tires
        # Steering angle  (i.e. 49 deg)
        self._max_steering_angle: float = 49 / 180 * math.pi  # In radians
        
        # Trailer and vehicle hierarchy
        self._trailer: Optional[Vehicle] = None
        """Create trailer object here, if the vehicle has a trailer. Set to None, if the vehicle has no trailer"""
        # Connection point must always be initialised with a value
        self._connection_point: float = 11.65  # meter from front
        
        # Vehicle type (init with True for standard vehicle)
        self._has_body: bool = True  # When false, the vehicle has no axles and no body (i.e. drawbar)
        self._has_front_axle: bool = True  # When false, no front axle will be drawn (i.e. semitrailer)
        self._has_rear_axle: bool = True  # When false, no rear axle will be drawn

        # Graphics
        self._symbol: str = ""  # Path to svg symbol relative to this file. Empty for generic vehicle
        self._symbol_size_x: float = 15.0 # SVG symbol size x in QGIS style units (usually meters)
        self._symbol_size_y: float = 2.5  # SVG symbol size y in QGIS style units (usually meters)
        # Offset to Place the symbol. Base point is point F.
        # SVG base point depends on the defined align in the QGIS style (normally center)
        # All in QGIS Style Units (normally meters)
        self._symbol_offset_x: float = -4.4
        self._symbol_offset_y: float = 0.0
        # Displaying steered wheels
        self._wheel_side_offset: float = self._axle_with / 2

        # **************************************************************************************************************
        # No setup for new vehicle necessary
        # Driving
        self._speed: float = 0.0
        self._steering_angle: float = 0.0
        self._trailer_angle: float = 0.0

        # Technical fields
        self._vehicle_is_placed: bool = False
        self._maximum_speed: float = 8.33
        self._vehicle_parts: list[Vehicle] = []  # All vehicle parts. Only used in main vehicle. Main vehicle is the first entry

        # Update the vehicle parts list
        self._update_vehicle_parts()

        # Setup vehicle shape
        self._init_vehicle_shape()


    def _init_vehicle_shape(self):
        # Vehicle local crs (polar from F)
        #   BL    RWLB            FWLB   FL
        #   +------+---------------+-----+
        #   |     RWL             FWL    |
        #   CP - - H - - - - - - - F - - +  Front (x direction)
        #   |     RWR             FWR    |
        #   +------+---------------+-----+
        #   BR    RWRB            FWRB   FR
        # Setup polar coordinates of the vehicle local crs
        # Necessary points
        # Setup rear reference point
        self._wheelbase: float = self._rear_axle_ref_pos - self._front_axle_ref_pos
        self._local_point_h: PolarCoord = CoordUtils.to_polar(- self._wheelbase, 0.0)
        # Setup connection point
        connection_point_distance: float = self._connection_point - self._front_axle_ref_pos
        self._local_point_cp: PolarCoord = CoordUtils.to_polar(- connection_point_distance, 0.0)

        # Setup body
        back_distance: float = self._body_length - self._front_axle_ref_pos
        body_side_offset: float = self._body_width / 2

        if self._has_body:
            self._local_point_bl: PolarCoord = CoordUtils.to_polar(- back_distance, body_side_offset)
            self._local_point_fl: PolarCoord = CoordUtils.to_polar(self._front_axle_ref_pos, body_side_offset)
            self._local_point_br: PolarCoord = CoordUtils.to_polar(- back_distance, - body_side_offset)
            self._local_point_fr: PolarCoord = CoordUtils.to_polar(self._front_axle_ref_pos, - body_side_offset)

            self._local_point_rwl: PolarCoord = CoordUtils.to_polar(- self._wheelbase, self._wheel_side_offset)
            self._local_point_rwr: PolarCoord = CoordUtils.to_polar(- self._wheelbase, - self._wheel_side_offset)
            self._local_point_rwlb: PolarCoord = CoordUtils.to_polar(- self._wheelbase, body_side_offset)
            self._local_point_rwrb: PolarCoord = CoordUtils.to_polar(- self._wheelbase, - body_side_offset)

        if self._has_body and self._has_front_axle:
            self._local_point_fwl: PolarCoord = CoordUtils.to_polar(0.0, self._wheel_side_offset)
            self._local_point_fwr: PolarCoord = CoordUtils.to_polar(0.0, - self._wheel_side_offset)
            self._local_point_fwlb: PolarCoord = CoordUtils.to_polar(0.0, body_side_offset)
            self._local_point_fwrb: PolarCoord = CoordUtils.to_polar(0.0, - body_side_offset)


    def _update_vehicle_parts(self):
        """
        Updates the vehicle parts list when the vehicle is a main vehicle
        Method is only called when creating the vehicle and when a trailer is added
        """    
        if self.is_main_vehicle:
            self._vehicle_parts = [self]
            child_vehicle = self._trailer
            while child_vehicle is not None:
                self._vehicle_parts.append(child_vehicle)
                child_vehicle = child_vehicle._trailer


    def _calc_azimuth(self) -> float:
        """Calculates the azimuth of the vehicle based on the points f and h

        @return: Azimuth of the vehicle (0.0 = facing east) in radians
        """
        dx = self._global_f.x - self._global_h.x
        dy = self._global_f.y - self._global_h.y
        return math.atan2(dy, dx)


    def _calc_angle_between_trailer(self) -> float:
        """Calculate the angle between the vehicle (self) and the trailer (_trailer)

        @return: Angle between vehicle and trailer (0.0 = straight) in radians
        """
        return self._global_a - self._trailer._global_a


    def _calc_global_coord(self, local_coord: PolarCoord, reference_point: CartesianCoord = None) -> CartesianCoord:
        """
        Calculate the global coordinate for a local polar coordinate
        Based on current position and rotation of the vehicle
        If the reference point not specified, the front wheel point f is used

        @param local_coord: The local coordinate as polar coordinate
        @return: The global coordinate
        """

        if not reference_point:
            reference_point = self._global_f

        new_azimuth: float = self._global_a + local_coord.a
        cartesian_shift: CartesianCoord = CoordUtils.to_cartesian(local_coord.d, new_azimuth)
        return cartesian_shift + reference_point


    def place_vehicle(self, f:CartesianCoord, a:float):
        """ 
        Place the vehicle at a given point and calculate the base point h
        This function is only needed at first vehicle placement
        During driving, the azimuth a is not known

        @param f: Coordinate of reference point f
        @param a: Azimuth of the vehicle (0.0 facing east)
        """         
        self._global_f = f
        self._global_a = a
        self._global_h = self._calc_global_coord(self._local_point_h)
        self._global_cp = self._calc_global_coord(self._local_point_cp)

        # Place trailer
        if self._trailer:
            self._trailer.place_vehicle(self._global_cp, self._global_a)

        self._vehicle_is_placed = True


    def _get_front_wheel_radius(self) -> float:
        """
        Calculate the radius, on which the front wheel point (f) drives
        Can only be calculated when the wheels are turned
        """
        return float(self._wheelbase / math.sin(self._steering_angle))

    # Not used since rear wheel path is calculated on straight segments
    # Function kept for later use when simulating rear wheel steering
    def _get_rear_wheel_radius(self) -> float:
        """
        Calculate the radius, on which the rear wheel point (h) drives
        Can only be calculated when the wheels are turned
        """
        return float(self._wheelbase / math.tan(self._steering_angle))

    def _get_center_angle(self, distance: float) -> float:
        """
        Calculate the center angle of one step.
        Calculation based on step distance of the front wheel point f along the driving arch
        @param distance: driving distance
        """
        return float(distance) / self._get_front_wheel_radius()

    def _get_driving_vector_front(self, distance: float) -> PolarCoord:
        center_angle = self._get_center_angle(distance)
        outer_angle = (math.pi - center_angle) / 2
        driving_vector_angle = math.pi / 2 - outer_angle + self.steering_angle
        driving_vector_distance = (self._get_front_wheel_radius() * math.sin(center_angle)) / math.sin(outer_angle)
        return PolarCoord(driving_vector_distance, driving_vector_angle)


    def _drive(self, distance: float):
        """
        Drive the vehicle one step
        """
        if abs(self._steering_angle) > 0.0:
            front_wheel_driving_vector: PolarCoord = self._get_driving_vector_front(distance)
        else:
            front_wheel_driving_vector = PolarCoord(distance, 0.0)

        # Calculate the global point f
        # Recalculate a and the other global points h and cp
        self._global_f = self._calc_global_coord(front_wheel_driving_vector)
        self._global_a = self._calc_azimuth()
        self._global_h = self._calc_global_coord(self._local_point_h)
        self._global_cp = self._calc_global_coord(self._local_point_cp)

        # Simulate trailer
        if self._trailer:
            self._trailer.step_trailer(self._global_cp, self._trailer_angle, distance)


    def step(self, distance: float):
        """
        Calculates the next point based on current location and steering angle
        @param distance: Distance to drive with one step
        """
        assert self._vehicle_is_placed, "Vehicle must be placed firs"
        if self._trailer: self._trailer_angle = self._calc_angle_between_trailer()
        self._drive(distance)


    def step_trailer(self, connection_point: CartesianCoord, vehicle_angle: float, distance: float):
        """
        Simulate the movement of a trailer based on connection point
        The connection point from the parent vehicle ist the reference point f of the trailer

        @param connection_point: Global cartesian coordinate of the connection point. Acts as point f of trailer
        @param vehicle_angle: Angle between parent vehicle and trailer. Acts as steering angle of trailer
        @param distance: Distance to drive with one step
        """
        assert self._vehicle_is_placed, "Vehicle must be placed first"
        self._global_f = connection_point
        self._steering_angle = vehicle_angle

        if self._trailer: self._trailer_angle = self._calc_angle_between_trailer()
        self._drive(distance)


    def speed_up(self, step: float):
        """
        Increase vehicle speed
        @param step: step to change the speed
        """
        self._speed += step
        # Speed limit of 25 km/h.
        # The maximum possible speed is dependent on the performance of QGIS. However, 25 km/h should not be exceeded.
        if self._speed >= self._maximum_speed:
            self.speed_down(step)


    def speed_down(self, step: float):
        """
        Decrease vehicle speed
        @param step: step to change the speed
        """
        self._speed -= step
        # Reversing speed limit of -25 km/h.
        # The maximum possible speed is dependent on the performance of QGIS. However, 25 km/h should not be exceeded.
        # Currently, reversing is not possible
        if self._speed <= -self._maximum_speed:
            self.speed_up(step)


    def steer_left(self, step: float):
        """
        Increase wheel angle, if the max steering angle is not exceeded
        @param step: Step to change wheel angle
        """
        new_angle = self._steering_angle + (step if self._steering_angle >= 0 else step)
        if self._max_steering_angle >= new_angle:
            self._steering_angle = new_angle


    def steer_right(self, step: float):
        """
        Increase wheel angle, if the max steering angle is not exceeded
        @param step: Step to change wheel angle
        """
        new_angle = self._steering_angle - (step if self._steering_angle <= 0 else step)
        if self._max_steering_angle * -1 <= new_angle:
            self._steering_angle = new_angle


    def get_symbol_path(self) -> str:
        """Returns the absolute file path of the symbol"""
        return str(Path(inspect.getfile(self.__class__)).parent / Path(self._symbol))


    @property
    def trailer(self):  # -> typing.Self Annotation removed for backward compatibility with Python 3.9
        """
        Trailer. Child vehicle object.
        If the Vehicle has no trailer parts. The value is None
        """
        return self._trailer
    
    @trailer.setter
    def trailer(self, v):  # v:typing.Self Annotation removed for backward compatibility with Python 3.9
        self._trailer = v
        # After a trailer is added. The list with all vehicle parts will be updated
        self._update_vehicle_parts()

    @property
    def vehicle_parts(self):  # -> list[typing.Self] Annotation removed for backward compatibility with Python 3.9
        """
        Only set on main vehicles (None for child vehicles i.e. trailers)
        First value is the main vehicle itself. After that all parts (even child of child) are stored
        List is used to draw the entire vehicle in a loop
        """
        return self._vehicle_parts

    @property
    def speed(self) -> float:
        """Current speed in m/s"""
        return self._speed

    @speed.setter
    def speed(self, v):
        """Sets the vehicle speed"""
        self._speed = v

    @property
    def steering_angle(self) -> float:
        """Current wheel angle in radians"""
        return self._steering_angle

    @steering_angle.setter
    def steering_angle(self, v):
        """Sets the steering angle"""
        self._steering_angle = v

    @property
    def f(self) -> CartesianCoord:
        """Global Coordinate of point f"""
        return self._global_f

    @property
    def h(self) -> CartesianCoord:
        """Global Coordinate of point h"""
        return self._global_h

    @property
    def a(self) -> float:
        """Vehicle azimuth in rad"""
        return self._global_a

    @property
    def bl(self) -> CartesianCoord:
        """Global Coordinate of point bl"""
        return self._calc_global_coord(self._local_point_bl)

    @property
    def rwl(self) -> CartesianCoord:
        """Global Coordinate of point rwl"""
        return self._calc_global_coord(self._local_point_rwl)

    @property
    def fwl(self) -> CartesianCoord:
        """Global Coordinate of point fwl"""
        return self._calc_global_coord(self._local_point_fwl)

    @property
    def fl(self) -> CartesianCoord:
        """Global Coordinate of point fl"""
        return self._calc_global_coord(self._local_point_fl)

    @property
    def br(self) -> CartesianCoord:
        """Global Coordinate of point br"""
        return self._calc_global_coord(self._local_point_br)

    @property
    def rwr(self) -> CartesianCoord:
        """Global Coordinate of point rwr"""
        return self._calc_global_coord(self._local_point_rwr)

    @property
    def fwr(self) -> CartesianCoord:
        """Global Coordinate of point fwr"""
        return self._calc_global_coord(self._local_point_fwr)

    @property
    def fr(self) -> CartesianCoord:
        """Global Coordinate of point fr"""
        return self._calc_global_coord(self._local_point_fr)

    @property
    def rwlb(self) -> CartesianCoord:
        """Global Coordinate of point rwlb"""
        return self._calc_global_coord(self._local_point_rwlb)

    @property
    def fwlb(self) -> CartesianCoord:
        """Global Coordinate of point fwlb"""
        return self._calc_global_coord(self._local_point_fwlb)

    @property
    def rwrb(self) -> CartesianCoord:
        """Global Coordinate of point rwrb"""
        return self._calc_global_coord(self._local_point_rwrb)

    @property
    def fwrb(self) -> CartesianCoord:
        """Global Coordinate of point fwrb"""
        return self._calc_global_coord(self._local_point_fwrb)

    @property
    def cp(self) -> CartesianCoord:
        """Global Coordinate of point cp"""
        return self._global_cp

    @property
    def symbol(self) -> str:
        """The relative path to the symbol used for drawing"""
        return self._symbol
    
    @property
    def symbol_size_x(self) -> float:
        """
        The x size of the svg symbol in QGIS style units
        x represents the vehicle length
        """
        return self._symbol_size_x
    
    @property
    def symbol_size_y(self) -> float:
        """
        The y size of the svg symbol in QGIS style units
        y represents the vehicle width
        """
        return self._symbol_size_y
    
    @property
    def symbol_offset_x(self) -> float:
        """
        Symbol offset x to place the symbol based on point f
        Value is in QGIS style units (normally meters)
        """
        return self._symbol_offset_x

    @property
    def symbol_offset_y(self) -> float:
        """
        Symbol offset y to place the symbol based on point f
        Value is in QGIS style units (normally meters)
        """
        return self._symbol_offset_y

    @property
    def max_steering_angle(self) -> float:
        """
        The maximum possible steering angle of the steered front axle in radians
        """
        return self._max_steering_angle

    @property
    def has_front_axle(self) -> bool:
        """
        Returns true if the vehicle has a front axle, which will also be drawn
        """
        return self._has_front_axle

    @property
    def has_body(self) -> bool:
        """
        Returns true if the vehicle has a body, which will also be drawn
        """
        return self._has_body

    @property
    def has_rear_axle(self) -> bool:
        """
        Returns true if the vehicle has a rear axle, which will also be drawn
        """
        return self._has_rear_axle

    @property
    def is_placed(self) -> bool:
        """
        Returns true, if the vehicle is placed
        """
        return self._vehicle_is_placed


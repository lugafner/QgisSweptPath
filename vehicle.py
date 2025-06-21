import math

from .coord import PolarCoord, CartesianCoord, CoordUtils
from .simple_logger import PathLogger


class Vehicle:
    def __init__(self):
        # **************************************************************************************************************
        # Vehicle input parameters. Setup for new vehicle extending this class
        self._vehicle_name: str = "VEHICLE"
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
        self._is_main_vehicle: bool = True # True for standard vehicle
        self._trailer: Vehicle = None  # Init with None for standard vehicle
        # Connection point must always be initialised with a value
        self._connection_point: float = 11.65  # meter from front
        
        # Vehicle type (init with True for standard vehicle)
        self._has_body: bool = True  # When false, the vehicle has no axles and no body (i.e. drawbar)
        self._has_front_axle: bool = True  # when false, no front axle will be drawn (i.e. semitrailer)

        # Graphics
        self._symbol: str = "./vehicles/vehicle.svg"
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
        self._speed: float = 1.0
        self._steering_angle: float = 0.0
        self._trailer_angle: float = 0.0

        # Technical fields
        self._vehicle_is_placed: bool = False
        self._do_drawing: bool = True
        self._speed_up_steps: float = 0.1  # Increase speed in m/s with each input
        self._speed_down_steps: float = 0.1  # Decrease speed in m/s with each input
        self._steer_in_steps: float = 1.0 / 180 * math.pi  # Turn in wheels with each input in rad
        self._steer_back_steps: float = 1.0 / 180 * math.pi  # Turn back wheels with each input in rad
        self._simulation_step: float = 0.05  # Distance to drive with each simulation step in m
        self._iteration_break: float = self._simulation_step / self._speed  # Break time between simulation steps (init with none for trailers)
        self._vehicle_parts: list[Vehicle] = []  # All vehicle parts. Only used in main vehicle. Main vehicle is the first entry

        # Update the vehicle parts list
        self._update_vehicle_parts()

        # Setup vehicle shape
        self._init_vehicle_shape()

        # Debugging
        self._path_logger = PathLogger()


    def _init_vehicle_shape(self):
        # Vehicle local crs (polar from F)
        #   BL     RWL             FWL   FL
        #   +------+---------------+-----+
        #   |                            |
        #   CP - - H - - - - - - - F - - +  Front (x direction)
        #   |                            |
        #   +------+---------------+-----+
        #   BR     RWR             FWR   FR
        # Setup polar coordinates of the vehicle local crs
        # Necessary points
        # Setup rear reference point
        self._wheelbase: float = self._rear_axle_ref_pos - self._front_axle_ref_pos
        self._local_point_h: PolarCoord = CoordUtils.to_polar(- self._wheelbase, 0.0)
        # Setup connection point
        connection_point_distance: float = self._connection_point - self._front_axle_ref_pos
        self._local_point_cp: PolarCoord = CoordUtils.to_polar(- connection_point_distance, 0.0)

        # Setup body
        if self._has_body:
            back_distance: float = self._body_length - self._front_axle_ref_pos
            body_side_offset: float = self._body_width / 2

            self._local_point_bl: PolarCoord = CoordUtils.to_polar(- back_distance, body_side_offset)
            self._local_point_rwl: PolarCoord = CoordUtils.to_polar(- self._wheelbase, self._wheel_side_offset)
            self._local_point_fl: PolarCoord = CoordUtils.to_polar(self._front_axle_ref_pos, body_side_offset)
            self._local_point_br: PolarCoord = CoordUtils.to_polar(- back_distance, - body_side_offset)
            self._local_point_rwr: PolarCoord = CoordUtils.to_polar(- self._wheelbase, - self._wheel_side_offset)
            self._local_point_fr: PolarCoord = CoordUtils.to_polar(self._front_axle_ref_pos, - self._wheel_side_offset)

        if self._has_body and self._has_front_axle:
            self._local_point_fwl: PolarCoord = CoordUtils.to_polar(0.0, self._wheel_side_offset)
            self._local_point_fwr: PolarCoord = CoordUtils.to_polar(0.0, - self._wheel_side_offset)

        # TODO: Remove, if the vehicle is always placed first
        # Initialise vehicle position
        # self._global_f = CartesianCoord(0.0, 0.0)  # Initialize reference point with 0, 0
        # self._global_h = CartesianCoord(- self._wheelbase, 0.0)
        # self._global_a: float = self._calc_azimuth()  # Initialize azimuth (get from f and h)
        # self._global_cp: CartesianCoord = self._calc_global_coord(self._local_point_cp)
        

    def _update_vehicle_parts(self):
        """
        Updates the vehicle parts list when the vehicle is a main vehicle
        Method is only called when creating the vehicle and when a trailer is added
        """    
        if self._is_main_vehicle:
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


    def _draw(self):
        if self._has_body: self._draw_body()
        if self._has_front_axle: self._draw_front_axle()


    def _draw_body(self):
        self._global_bl: CartesianCoord = self._calc_global_coord(self._local_point_bl)
        self._global_fl: CartesianCoord = self._calc_global_coord(self._local_point_fl)
        self._global_br: CartesianCoord = self._calc_global_coord(self._local_point_br)
        self._global_fr: CartesianCoord = self._calc_global_coord(self._local_point_fr)
        self._global_rwl: CartesianCoord = self._calc_global_coord(self._local_point_rwl)
        self._global_rwr: CartesianCoord = self._calc_global_coord(self._local_point_rwr)


    def _draw_front_axle(self):
        self._global_fwl: CartesianCoord = self._calc_global_coord(self._local_point_fwl)
        self._global_fwr: CartesianCoord = self._calc_global_coord(self._local_point_fwr)


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

        # Draw the rest of the body points
        if self._do_drawing: self._draw()

        self._vehicle_is_placed = True


    def _get_front_wheel_radius(self) -> float:
        """
        Calculate the radius, on which the front wheel point (f) drives
        Can only be calculated when the wheels are turned
        """
        return float(self._wheelbase / math.cos(math.pi / 2.0 - self._steering_angle))


    def _get_rear_wheel_radius(self) -> float:
        """
        Calculate the radius, on which the rear wheel point (h) drives
        Can only be calculated when the wheels are turned
        """
        return float(self._wheelbase * math.tan(math.pi / 2.0 - self._steering_angle))

    def _get_center_angle(self) -> float:
        """
        Calculate the center angle of one step.
        Calculation based on step distance of the rear wheel point h along the driving arch
        """
        return float(self._simulation_step / self._get_rear_wheel_radius())

    def _get_driving_vector_front(self) -> PolarCoord:
        center_angle = self._get_center_angle()
        outer_angle = (math.pi - center_angle) / 2
        driving_vector_angle = math.pi / 2 - outer_angle + self.steering_angle
        driving_vector_distance = (self._get_front_wheel_radius() * math.sin(center_angle)) / math.sin(outer_angle)
        return PolarCoord(driving_vector_distance, driving_vector_angle)

    def _get_driving_vector_rear(self) -> PolarCoord:
        center_angle = self._get_center_angle()
        outer_angle = (math.pi  - center_angle) / 2
        driving_vector_angle = (math.pi / 2) - outer_angle
        driving_vector_distance = (self._get_rear_wheel_radius() * math.sin(center_angle)) / math.sin(outer_angle)
        return PolarCoord(driving_vector_distance, driving_vector_angle)


    def _drive(self):
        """
        Drive the vehicle one step
        """
        if abs(self._steering_angle) > 0.0:
            front_wheel_driving_vector: PolarCoord = self._get_driving_vector_front()
            rear_wheel_driving_vector: PolarCoord = self._get_driving_vector_rear()
        else:
            front_wheel_driving_vector = PolarCoord(self._simulation_step, 0.0)
            rear_wheel_driving_vector = PolarCoord(self._simulation_step, 0.0)

        # Calculate the global points f and h
        self._global_f = self._calc_global_coord(front_wheel_driving_vector)
        self._global_h = self._calc_global_coord(rear_wheel_driving_vector, self._global_h)


        # Log path
        self._path_logger.write_log(
            self._get_front_wheel_radius(),
            self._get_rear_wheel_radius(),
            self._get_center_angle(),
            self.steering_angle,
            self._wheelbase,
            self._global_a,
            self._global_f.x,
            self._global_f.y,
            self._global_h.x,
            self._global_h.y
        )

        # After calculating the points f and h, the global vehicle azimuth must be recalculated
        # before the other coordinates are calculated
        self._global_a = self._calc_azimuth()
        self._global_cp = self._calc_global_coord(self._local_point_cp)

        # Draw the rest of the body points
        if self._do_drawing: self._draw()

        # Simulate trailer
        if self._trailer:
            self._trailer.step_trailer(self._global_cp, self._trailer_angle)


    def step(self):
        """
        Calculates the next point based on current location and steering angle
        """
        assert self._vehicle_is_placed, "Vehicle must be placed firs"
        if self._trailer: self._trailer_angle = self._calc_angle_between_trailer()
        self._drive()


    def step_trailer(self, connection_point: CartesianCoord, vehicle_angle: float):
        """
        Simulate the movement of a trailer based on connection point
        The connection point from the parent vehicle ist the reference point f of the trailer

        @param connection_point: Global cartesian coordinate of the connection point. Acts as point f of trailer
        @param vehicle_angle: Angle between parent vehicle and trailer. Acts as steering angle of trailer
        """
        assert self._vehicle_is_placed, "Vehicle must be placed first"
        self._global_f = connection_point
        self._steering_angle = vehicle_angle

        if self._trailer: self._trailer_angle = self._calc_angle_between_trailer()
        self._drive()


    def speed_up(self):
        """Increase vehicle speed"""
        self._speed += self._speed_up_steps
        # Speed limit of 25 km/h.
        # The maximum possible speed is dependent on the performance of QGIS. However, 25 km/h should not be exceeded.
        if self._speed >= 6.94:
            self.speed_down()

    def speed_down(self):
        """Decrease vehicle speed"""
        self._speed -= self._speed_down_steps
        # Reversing speed limit of -25 km/h.
        # The maximum possible speed is dependent on the performance of QGIS. However, 25 km/h should not be exceeded.
        # Currently, reversing is not possible
        if self._speed <= -6.94:
            self.speed_up()

    def steer_left(self):
        """Increase wheel angle, if the max steering angle is not exceeded"""
        new_angle = self._steering_angle + (self._steer_in_steps if self._steering_angle >= 0 else self._steer_back_steps)
        if self._max_steering_angle >= new_angle:
            self._steering_angle = new_angle

    def steer_right(self):
        """Increase wheel angle, if the max steering angle is not exceeded"""
        new_angle = self._steering_angle - (self._steer_in_steps if self._steering_angle <= 0 else self._steer_back_steps)
        if self._max_steering_angle * -1 <= new_angle:
            self._steering_angle = new_angle

    # Properties
    @property
    def do_drawing(self) -> bool:
        """
        Specify if the vehicle body should be drawn
        For normal vehicle parts set to True (default). False only used i.e. for drawbar
        """
        return self._do_drawing
    
    @do_drawing.setter
    def do_drawing(self, v: bool):
        self._do_drawing = v

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

    @property
    def steering_angle(self) -> float:
        """Current wheel angle in radians"""
        return self._steering_angle

    @property
    def simulation_step(self) -> float:
        """Driving distance with each simulation step in meters"""
        return self._simulation_step

    @simulation_step.setter
    def simulation_step(self, v:float):
        """Set distance to drive with each simulation step in meters"""
        self._simulation_step = v

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
        return self._global_bl

    @property
    def rwl(self) -> CartesianCoord:
        """Global Coordinate of point rwl"""
        return self._global_rwl

    @property
    def fwl(self) -> CartesianCoord:
        """Global Coordinate of point fwl"""
        return self._global_fwl

    @property
    def fl(self) -> CartesianCoord:
        """Global Coordinate of point fl"""
        return self._global_fl

    @property
    def br(self) -> CartesianCoord:
        """Global Coordinate of point br"""
        return self._global_br

    @property
    def rwr(self) -> CartesianCoord:
        """Global Coordinate of point rwr"""
        return self._global_rwr

    @property
    def fwr(self) -> CartesianCoord:
        """Global Coordinate of point fwr"""
        return self._global_fwr

    @property
    def fr(self) -> CartesianCoord:
        """Global Coordinate of point fr"""
        return self._global_fr

    @property
    def cp(self) -> CartesianCoord:
        """Global Coordinate of point cp"""
        return self._global_cp

    @property
    def symbol(self) -> str:
        """The path to the symbol used for drawing"""
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
    def is_main_vehicle(self) -> bool:
        """
        Returns true, if the vehicle is the main vehicle
        The main vehicle is the driven vehicle. This vehicle could tow a trailer
        """
        return self._is_main_vehicle

    @property
    def is_placed(self) -> bool:
        """
        Returns true, if the vehicle is placed
        """
        return self._vehicle_is_placed

    @property
    def vehicle_name(self) -> str:
        """
        Returns the vehicle name
        """
        return self._vehicle_name

from coord import PolarCoord, CartesianCoord, CoordUtils


class Vehicle:
    def __init__(self):
        """Constructor"""
        
        # Vehicle input parameters
        # Body
        self._body_length:  float = 15.00  # meter
        self._body_width: float = 2.50  # meter
        
        # Chassis
        self._front_axle_ref_pos: float = 3.10  # meter from front
        self._rear_axle_ref_pos: float = 11.65  # meter from front
        self._axle_with: float = 2.50  # meter
        
        # Steering
        self._max_steering_angle = 53.0  # degrees

        # Further initialisation
        self._init_fehicle_coords()
        

    def _init_fehicle_coords(self):
        """Initialises the vehicle coordinates"""
        # Calculated parameters
        wheelbase = self._rear_axle_ref_pos - self._front_axle_ref_pos
        back_distanz = self._body_length - self._front_axle_ref_pos
        wheel_side_offset = self._axle_with / 2
        body_side_offset = self._body_width / 2

        # Vehicle local crs (polar)
        #   BL    RWL             FWL   FL
        #   +-----+---------------+-----+
        #   |                           |
        #   + - - H - - - - - - - F - - +  Front
        #   |                           |
        #   +-----+---------------+-----+
        #   BR    RWR             FWR   FR
        self._local_point_h = CoordUtils.toPolar(- wheelbase, 0)
        self._local_point_bl = CoordUtils.toPolar(- back_distanz, body_side_offset)
        self._local_point_rwl = CoordUtils.toPolar(- wheelbase, wheel_side_offset)
        self._local_point_fwl = CoordUtils.toPolar(0, wheel_side_offset)
        self._local_point_fl = CoordUtils.toPolar(self._front_axle_ref_pos, body_side_offset)
        self._local_point_br = CoordUtils.toPolar(- back_distanz, - body_side_offset)
        self._local_point_rwr = CoordUtils.toPolar(- wheelbase, - wheel_side_offset)
        self._local_point_fwr = CoordUtils.toPolar(0, - wheel_side_offset)
        self._local_point_fr = CoordUtils.toPolar(self._front_axle_ref_pos, - wheel_side_offset)
        
        # Fehicle position
        self._front_axle_ref_pos = CartesianCoord(0, 0)  # Initialize reference point with 0, 0
        self._azimuth: float = 0.0  # Initialize azimuth with 0 degrees


    def _transform_to_global(source: PolarCoord) -> CartesianCoord:
        """
        @source: Coordinate to transform
        """
        pass
    
        
           
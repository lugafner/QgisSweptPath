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
        self._wheelbase = self._rear_axle_ref_pos - self._front_axle_ref_pos

        # Vehicle local crs (polar)
        #   BL    RWL             FWL   FL
        #   +-----+---------------+-----+
        #   |                           |
        #   + - - H - - - - - - - F - - +  Front
        #   |                           |
        #   +-----+---------------+-----+
        #   BR    RWR             FWR   FR
        self._local_point_h = CoordUtils.polarFromShift()
        self._local_point_bl = PolarCoord()
        self._local_point_rwl = PolarCoord()
        self._local_point_fwl = PolarCoord()
        self._local_point_fl = PolarCoord()
        self._local_point_br = PolarCoord()
        self._local_point_rwr = PolarCoord()
        self._local_point_fwr = PolarCoord()
        self._local_point_fr = PolarCoord()
        
        # Fehicle position
        self._front_axle_ref_pos = CartesianCoord(0, 0)  # Initialize reference point with 0, 0
        self._azimuth: float = 0.0  # Initialize azimuth with 0 degrees


    def _transform_to_global(source: PolarCoord) -> CartesianCoord:
        """
        @source: Coordinate to transform
        """
        pass
    
        
           
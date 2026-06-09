
# Vehicle Mercedes Citaro G
from ..vehicle import Vehicle
from .mercedes_citaro_g_trailer import MercedesCitaroGTrailer
import math

class MercedesCitaroG(Vehicle):
    vehicle_name = "Mercedes Citaro G"
    is_main_vehicle = True

    def __init__(self):
        super().__init__()

        # Set up all needed parameters
        # Body
        self._body_length = 9.744  # meter
        self._body_width = 2.550  # meter

        # Chassis
        self._front_axle_ref_pos = 2.805  # meter from front
        self._rear_axle_ref_pos = 8.705  # meter from front
        self._axle_with = 2.40  # meter incl. tires. ZF RL 82 EC

        # Turning circle diameter
        self._turning_circle: float = 19.16 # meter

        # Trailer and vehicle hierarchy
        self.trailer = MercedesCitaroGTrailer()  # Trailer. Always use setter of property
        self._connection_point = 10.530  # meter from front
        self._max_trailer_angle: float = 54.0 / 180 * math.pi  # Maximum trailer angle in radians

        # Vehicle type
        self._has_body = True
        self._has_front_axle  = True
        self._has_rear_axle = True

        # Graphics
        self._symbol = "./mercedes_citaro_g.svg"
        self._symbol_size_x = 10.530  # SVG symbol size x in QGIS style units (usually meters)
        self._symbol_size_y = 2.550  # SVG symbol size y in QGIS style units (usually meters)
        # Offset to Place the symbol. Base point is point F.
        # SVG base point depends on the defined align in the QGIS style (normally center)
        # All in QGIS Style Units (normally meters)
        self._symbol_offset_x = -2.460
        self._symbol_offset_y = 0.0
        # Displaying steered wheels
        self._wheel_side_offset = self._axle_with / 2

        # Update the vehicle parts list
        self._update_vehicle_parts()

        # Setup vehicle shape
        self._init_vehicle_shape()

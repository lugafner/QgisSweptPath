
# Vehicle Mercedes Citaro
from ..vehicle import Vehicle
import math

class MercedesCitaro(Vehicle):
    vehicle_name = "Mercedes Citaro K"
    is_main_vehicle = True  # solo bus

    def __init__(self):
        super().__init__()

        # Set up all needed parameters
        # Body
        self._body_length = 10.633  # meter
        self._body_width = 2.550  # meter

        # Chassis
        self._front_axle_ref_pos = 2.805  # meter from front
        self._rear_axle_ref_pos = 7.203  # meter from front
        self._axle_with = 2.40  # meter incl. tires. ZF RL 82 EC

        # Turning circle diameter
        self._turning_circle: float = 13.138 # meter

        # Trailer and vehicle hierarchy
        self.trailer = None  # solo bus

        # Vehicle type
        self._has_body = True
        self._has_front_axle  = True
        self._has_rear_axle = True

        # Graphics
        self._symbol = "./mercedes_citaro_k.svg"
        self._symbol_size_x = 10.633  # SVG symbol size x in QGIS style units (usually meters)
        self._symbol_size_y = 2.550  # SVG symbol size y in QGIS style units (usually meters)
        # Offset to Place the symbol. Base point is point F.
        # SVG base point depends on the defined align in the QGIS style (normally center)
        # All in QGIS Style Units (normally meters)
        self._symbol_offset_x = -2.5115
        self._symbol_offset_y = 0.0
        # Displaying steered wheels
        self._wheel_side_offset = self._axle_with / 2

        # Update the vehicle parts list
        self._update_vehicle_parts()

        # Setup vehicle shape
        self._init_vehicle_shape()

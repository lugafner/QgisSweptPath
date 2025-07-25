
# Vehicle Doppelgelenkbus 24.66m (Hess Trolleybus)
from ..vehicle import Vehicle
import math

class Doppelgelenkbus2466(Vehicle):
    vehicle_name = "Doppelgelenkbus 24.66m"
    is_main_vehicle = True
    
    def __init__(self):
        super().__init__()

        # Set up all needed parameters
        # Vehicle geometry based on template from canton of lucerne
        # Body
        self._body_length = 9.571  # meter
        self._body_width = 2.55  # meter

        # Chassis
        self._front_axle_ref_pos = 2.731  # meter from front
        self._rear_axle_ref_pos = 8.576  # meter from front
        self._axle_with = 2.55  # meter incl. tires

        # Steering angle (inner 53 deg, outer 46 deg, mean 49.5 deg). Based on Mercedes Citaro
        self._max_steering_angle = 49.5 / 180 * math.pi  # In radians

        # Trailer and vehicle hierarchy
        self.trailer = None  # solo bus
        self._connection_point = 10.401  # meter from front

        # Vehicle type
        self._has_body = True
        self._has_front_axle  = True
        self._has_rear_axle = True

        # Graphics
        self._symbol = "./doppelgelenkbus_24_66.svg"
        self._symbol_size_x = 10.401  # SVG symbol size x in QGIS style units (usually meters)
        self._symbol_size_y = 2.550  # SVG symbol size y in QGIS style units (usually meters)
        # Offset to Place the symbol. Base point is point F.
        # SVG base point depends on the defined align in the QGIS style (normally center)
        # All in QGIS Style Units (normally meters)
        self._symbol_offset_x = -2.4695
        self._symbol_offset_y = 0.0
        # Displaying steered wheels
        self._wheel_side_offset = self._axle_with / 2

        # Update the vehicle parts list
        self._update_vehicle_parts()

        # Setup vehicle shape
        self._init_vehicle_shape()

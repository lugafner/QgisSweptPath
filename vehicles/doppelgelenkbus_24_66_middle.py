
# Vehicle Doppelgelenkbus 24.66m Hess Trolleybus (Middle section)
from ..vehicle import Vehicle
from .doppelgelenkbus_24_66_tail import Doppelgelenkbus2466Tail

class Doppelgelenkbus2466Middle(Vehicle):
    vehicle_name = "Doppelgelenkbus 24.66m Middle"
    is_main_vehicle = False  # Trailer
    
    def __init__(self):
        super().__init__()

        # Set up all needed parameters
        # Vehicle geometry based on template from canton of lucerne
        # Body
        self._body_length = 5.758  # meter
        self._body_width = 2.55  # meter

        # Chassis
        self._front_axle_ref_pos = -0.83  # meter from front
        self._rear_axle_ref_pos = 4.043  # meter from front
        self._axle_with = 2.55  # meter incl. tires. ZF RL 82 EC

        # Steering angle (inner 53 deg, outer 46 deg, mean 49.5 deg)
        self._max_steering_angle = 0.0  # Not needed for trailer

        # Trailer and vehicle hierarchy
        self.trailer = Doppelgelenkbus2466Tail()
        self._connection_point = 6.588  # meter from front (negative = point is in front of vehicle)

        # Vehicle type
        self._has_body = True
        self._has_front_axle  = False
        self._has_rear_axle = True

        # Graphics
        self._symbol = "./doppelgelenkbus_24_66_middle.svg"
        self._symbol_size_x = 7.418  # SVG symbol size x in QGIS style units (usually meters)
        self._symbol_size_y = 2.55  # SVG symbol size y in QGIS style units (usually meters)
        # Offset to Place the symbol. Base point is point F.
        # SVG base point depends on the defined align in the QGIS style (normally center)
        # All in QGIS Style Units (normally meters)
        self._symbol_offset_x = -3.709
        self._symbol_offset_y = 0.0
        # Displaying steered wheels
        self._wheel_side_offset = self._axle_with / 2

        # Update the vehicle parts list
        self._update_vehicle_parts()

        # Setup vehicle shape
        self._init_vehicle_shape()

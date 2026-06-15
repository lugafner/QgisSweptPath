
# Vehicle Mercedes Citaro G (Trailer)
from ..vehicle import Vehicle

class MercedesCitaroGTrailer(Vehicle):
    vehicle_name = "Mercedes Citaro G Trailer"
    is_main_vehicle = False  # Trailer

    def __init__(self):
        super().__init__()

        # Set up all needed parameters
        # Body
        self._body_length = 6.809  # meter
        self._body_width = 2.550  # meter

        # Chassis
        self._front_axle_ref_pos = -0.786 # meter from front
        self._rear_axle_ref_pos = 3.379  # meter from front
        self._axle_with = 2.40  # meter incl. tires. ZF RL 82 EC

        # Trailer and vehicle hierarchy
        self.trailer = None  # No trailer
        self._connection_point = -0.786  # meter from front (negative = point is in front of vehicle)

        # Vehicle type
        self._has_body = True
        self._has_front_axle  = False
        self._has_rear_axle = True

        # Graphics
        self._symbol = "./mercedes_citaro_g_trailer.svg"
        self._symbol_size_x = 7.595  # SVG symbol size x in QGIS style units (usually meters)
        self._symbol_size_y = 2.550  # SVG symbol size y in QGIS style units (usually meters)
        # Offset to Place the symbol. Base point is point F.
        # SVG base point depends on the defined align in the QGIS style (normally center)
        # All in QGIS Style Units (normally meters)
        self._symbol_offset_x = -3.7975
        self._symbol_offset_y = 0.0
        # Displaying steered wheels
        self._wheel_side_offset = self._axle_with / 2

        # Update the vehicle parts list
        self._update_vehicle_parts()

        # Setup vehicle shape
        self._init_vehicle_shape()

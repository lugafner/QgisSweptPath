from enum import IntEnum

class SimulationMode(IntEnum):
    STEP_BASED = 0
    FRAME_BASED = 1


class BorderDistanceUnits(IntEnum):
    MAP_UNITS = 0
    PIXELS = 1
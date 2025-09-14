from enum import IntEnum, Enum

class SimulationMode(IntEnum):
    STEP_BASED = 0
    FRAME_BASED = 1


class BorderDistanceUnits(IntEnum):
    MAP_UNITS = 0
    PIXELS = 1


class VehicleStatusType(Enum):
    UNDEFINED_ERROR = 0
    MAX_ANGLE = 1


class VehicleStatusAction(Enum):
    STOP = 0
    PAUSE = 1

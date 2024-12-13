from vehicle import Vehicle
from coord import CartesianCoord
import math

v = Vehicle()

azi = 0

v.place_vehicle(CartesianCoord(0, 0), azi / 180 * math.pi)

print(v._global_h)

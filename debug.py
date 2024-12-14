from vehicle import Vehicle
from coord import CartesianCoord
import math

v_parent = Vehicle()
v_trailer = Vehicle()

v_parent._trailer = v_trailer


azi = 0.0
steer = 45.0

v_parent.place_vehicle(CartesianCoord(0.0, 0.0), azi / 180 * math.pi)
print(str(v_parent._global_h.x) + "," + 
      str(v_parent._global_h.y) + "," +
      str(v_parent._global_f.x) + "," +
      str(v_parent._global_f.y) + "," +
      str(v_trailer._global_h.x) + "," + 
      str(v_trailer._global_h.y) + "," +
      str(v_trailer._global_f.x) + "," +
      str(v_trailer._global_f.y))

for i in range(40):
    v_parent.step(steer, 0.5)
    print(str(v_parent._global_h.x) + "," + 
        str(v_parent._global_h.y) + "," +
        str(v_parent._global_f.x) + "," +
        str(v_parent._global_f.y) + "," +
        str(v_trailer._global_h.x) + "," + 
        str(v_trailer._global_h.y) + "," +
        str(v_trailer._global_f.x) + "," +
        str(v_trailer._global_f.y))


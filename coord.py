from math import atan, sin

class PolarCoord:
    def __init__(self, d: float=0.0, a : float=0.0):
        self._d: float = d
        self._a: float = a

    @property
    def d(self):
        return self._x
    
    @d.setter
    def d(self, value):
        self._x = value
        
    @property
    def a(self):
        return self._y
    
    @a.setter
    def a(self, value):
        self._y = value
    

class CartesianCoord:
    def __init__(self, x: float=0.0, y: float=0.0):
        self._x: float = x
        self._y: float = y

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
    
class CoordUtils:
    def __init__(self):
        """Pass Constructor. Only static functions"""
        pass

    @staticmethod
    def polarFromShift(dx: float, dy: float) -> PolarCoord:
        polar: PolarCoord = PolarCoord()
        polar.a = atan(dx / dy)
        polar.d = dx / sin(polar.a)
        return polar

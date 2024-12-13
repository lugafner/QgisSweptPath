import math

class PolarCoord:
    def __init__(self, d: float=0.0, a : float=0.0):
        self._d: float = d
        self._a: float = a

    def __eq__(self, value):
        return (isinstance(value, PolarCoord) and 
                (round(self.d, 6) == round(value.d, 6)) and
                (round(self.a, 6) == round(value.a, 6)))

    def toCartesian(self):
        return CoordUtils.toCartesian(self._d, self._a)

    @property
    def d(self):
        return self._d
    
    @d.setter
    def d(self, value):
        self._d = value
        
    @property
    def a(self):
        return self._a
    
    @a.setter
    def a(self, value):
        self._a = value
    

class CartesianCoord:
    def __init__(self, x: float=0.0, y: float=0.0):
        self._x: float = x
        self._y: float = y

    def __eq__(self, value):
        return (isinstance(value, CartesianCoord) and 
                (round(self.x, 6) == round(value.x, 6)) and
                (round(self.y, 6) == round(value.y, 6)))

    def toPolar(self):
        return CoordUtils.toPolar(self._x, self._y)

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
    def toPolar(dx: float, dy: float) -> PolarCoord:
        polar: PolarCoord = PolarCoord()
        polar.a = math.atan2(dy, dx)
        polar.d = math.sqrt(dx**2 + dy**2)

        print(polar.a)
        print(polar.d)

        return polar
    
    @staticmethod
    def toCartesian(d: float, a: float) -> CartesianCoord:
        cartesian: CartesianCoord = CartesianCoord()
        print(a)

        cartesian.x = d * math.cos(a)
        cartesian.y = d * math.sin(a)

        print(cartesian.x)
        print(cartesian.y)

        return cartesian

import math

class PolarCoord:
    def __init__(self, d: float=0.0, a : float=0.0):
        self._d: float = d
        self._a: float = a

    def __eq__(self, value):
        return (isinstance(value, PolarCoord) and 
                (round(self.d, 6) == round(value.d, 6)) and
                (round(self.a, 6) == round(value.a, 6)))
    
    def __str__(self):
        return f"d = {self.d}, a = {self.a}"

    def to_cartesian(self):
        return CoordUtils.to_cartesian(self.d, self.a)

    @property
    def d(self):
        return self._d
        
    @property
    def a(self):
        return self._a
    

class CartesianCoord:
    def __init__(self, x: float=0.0, y: float=0.0):
        self._x: float = x
        self._y: float = y

    def __eq__(self, value):
        return (isinstance(value, CartesianCoord) and 
                (round(self.x, 6) == round(value.x, 6)) and
                (round(self.y, 6) == round(value.y, 6)))
    
    def __str__(self):
        return f"x = {self.x}, y = {self.y}"

    def __add__(self, value):
        if isinstance(value, CartesianCoord):
            return CartesianCoord(
                x=self._x + value.x,
                y=self._y + value.y
            )
        else:
            raise TypeError(f"The object {value} is not a {type(self)}.")
        
    def __sub__(self, value):
        if isinstance(value, CartesianCoord):
            return CartesianCoord(
                x=self._x - value.x,
                y=self._y - value.y
            )
        else:
            raise TypeError(f"The object {value} is not a {type(self)}.")

    def to_polar(self):
        return CoordUtils.to_polar(self.x, self.y)

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    

class CoordUtils:
    def __init__(self):
        """Pass Constructor. Only static functions"""
        pass

    @staticmethod
    def to_polar(dx: float, dy: float) -> PolarCoord:
        """Creates a polar coordinat from delta x and delta y

        @param dx: Delta x
        @param dy: Delta y
        @return: Polar coordinate (0.0rad = east)
        """        
        return PolarCoord(
            a=math.atan2(dy, dx),
            d=math.sqrt(dx**2 + dy**2))
    
    @staticmethod
    def to_cartesian(d: float, a: float) -> CartesianCoord:
        """Creates a cartesian coordinate from a distance and angle

        @param d: Distance
        @param a: Angle (0.0rad = east)
        @return: Cartesian coordinate (x = east, y = north)
        """    
        return CartesianCoord(
            x=d * math.cos(a),
            y=d * math.sin(a))

    @staticmethod
    def rad_to_degrees(a: float) -> float:
        """ Converts radians into degrees. This function keeps the sign.

        @param a: Angle in radians
        @return Angel in degrees
        """
        return a * 180.0 / math.pi

    @staticmethod
    def degrees_to_rad(a: float) -> float:
        """ Converts degrees into radians. This function keeps the sign.

        @param a: Angle in degrees
        @return Angle in radians
        """
        return a * math.pi / 180.0
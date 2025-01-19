from coord import CartesianCoord, PolarCoord, CoordUtils
import unittest

class TestCoordConversion(unittest.TestCase):
    def testConversion(self):
        coord1q = CartesianCoord(3, 3)
        coord2q = CartesianCoord(3, -3)
        coord3q = CartesianCoord(-3, -3)
        coord4q = CartesianCoord(-3 ,3)

        self.assertEqual(coord1q.to_polar().to_cartesian(), coord1q)
        self.assertEqual(coord2q.to_polar().to_cartesian(), coord2q)
        self.assertEqual(coord3q.to_polar().to_cartesian(), coord3q)
        self.assertEqual(coord4q.to_polar().to_cartesian(), coord4q)


class TestCoordCalculations(unittest.TestCase):
    def testCartesianAddition(self):
        coord1 = CartesianCoord(-1, 2)
        coord2 = CartesianCoord(4, -8)
        self.assertEqual(coord1 + coord2, CartesianCoord(3, -6))

    def testCartesianSubtraction(self):
        coord1 = CartesianCoord(-1, 2)
        coord2 = CartesianCoord(4, -8)
        self.assertEqual(coord1 - coord2, CartesianCoord(-5, 10))


if __name__ == '__main__':
    unittest.main()
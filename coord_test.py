from coord import CartesianCoord, PolarCoord, CoordUtils
import unittest

class TestCoordConversion(unittest.TestCase):
    def testConversion(self):
        coord1q = CartesianCoord(3, 3)
        coord2q = CartesianCoord(3, -3)
        coord3q = CartesianCoord(-3, -3)
        coord4q = CartesianCoord(-3 ,3)

        self.assertEqual(coord1q.toPolar().toCartesian(), coord1q)
        self.assertEqual(coord2q.toPolar().toCartesian(), coord2q)
        self.assertEqual(coord3q.toPolar().toCartesian(), coord3q)
        self.assertEqual(coord4q.toPolar().toCartesian(), coord4q)


if __name__ == '__main__':
    unittest.main()
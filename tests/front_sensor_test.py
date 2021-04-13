import distance_sensor_test
import unittest


class FrontSensorTest(distance_sensor_test.DistanceSensorTest):
    def __init__(self):
        super().__init__(echo=23, trigger=24)


if __name__ == '__main__':
    unittest.main()

import unittest
from gpiozero import DistanceSensor


class DistanceSensorTest(unittest.TestCase):
    def __init__(self, echo, trigger):
        super().__init__()
        self.__front_sensor = DistanceSensor(echo=echo, trigger=trigger, threshold_distance=0.1)

    def test_check_inactive(self):
        self.assertFalse(self.__front_sensor.is_active)

    def test_toggle_active(self):
        print('Activate the sensor now')
        self.__front_sensor.wait_for_active()
        print('Deactivate the sensor now')
        self.__front_sensor.wait_for_inactive()

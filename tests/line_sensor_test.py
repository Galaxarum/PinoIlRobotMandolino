import unittest

from gpiozero import DigitalInputDevice


class LineSensorTest(unittest.TestCase):

    def __init__(self):
        super().__init__()
        self.__line_sensor = DigitalInputDevice(4)

    def test_check_inactive(self):
        self.assertFalse(self.__line_sensor.is_active)

    def test_ask_for_status_toggle(self):
        print('Activate the sensor')
        self.__line_sensor.wait_for_active()
        print('Deactivate the sensor')
        self.__line_sensor.wait_for_inactive()


if __name__ == '__main__':
    unittest.main()

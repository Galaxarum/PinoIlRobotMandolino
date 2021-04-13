from gpiozero import DigitalInputDevice

from sensor_test import SensorTest


class LineSensorTest(SensorTest):
    def __init__(self):
        super().__init__(name='line sensor', sensor=DigitalInputDevice(4))

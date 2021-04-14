from gpiozero import LineSensor

from sensor_test import SensorTest


class LineSensorTest(SensorTest):
    def __init__(self):
        super().__init__(name='line sensor', sensor=LineSensor(4))

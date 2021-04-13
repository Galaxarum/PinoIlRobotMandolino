from gpiozero import DistanceSensor
from sensor_test import SensorTest


class DistanceSensorTest(SensorTest):
    def __init__(self, echo, trigger, name):
        super().__init__(name=name, sensor=DistanceSensor(echo=echo, trigger=trigger, threshold_distance=0.1))


class FrontSensorTest(DistanceSensorTest):
    def __init__(self):
        super().__init__(name='front sensor', echo=23, trigger=24)
        
        
class BackSensorTest(DistanceSensorTest):
    def __init__(self):
        super().__init__(name='back sensor', echo=2, trigger=3)
        

class LeftSensorTest(DistanceSensorTest):
    def __init__(self):
        super().__init__(name='back sensor', echo=25, trigger=8)
        
        
class RightSensorTest(DistanceSensorTest):
    def __init__(self):
        super().__init__(name='back sensor', echo=27, trigger=22)
        
        
# This just checks if all the sensors can be instantiated properly. Actual behaviour must be checked manually
if __name__ == "__main__":
    FrontSensorTest()
    BackSensorTest()
    LeftSensorTest()
    RightSensorTest()

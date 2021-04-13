from gpiozero import DistanceSensor


class DistanceSensorTest:
    def __init__(self, echo, trigger, name):
        self.__sensor = DistanceSensor(echo=echo, trigger=trigger, threshold_distance=0.1)
        self.__name = name
        
    def print_state(self):
        print(f'{self.__name} is {"active" if self.__sensor.is_active else "inactive"}')
        
    def check_activation(self):
        if self.__sensor.is_active:
            print(f'{self.__name} already activated')
            return
        print(f'Activate {self.name}')
        self.__sensor.wait_for_active()
        print(f'{self.__name} correctly activated')
        
    def check_deactivation(self):
        if not self.__sensor.is_active:
            print(f'{self.__name} not activated')
            return
        print(f'Deactivate {self.__name}')
        self.__sensor.wait_for_inactive()
        print(f'{self.__name} correctly deactivated')



class FrontSensorTest(DistanceSensorTest):
    def __init__(self):
        super().__init__(name='front sensor', echo=23, trigger=24)
        
        
class BackSensorTest(DistanceSensorTest):
    def __init__(self):
        super().__init__(name='back sensor', echo=2, trigger=3)
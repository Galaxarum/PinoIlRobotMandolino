from gpiozero import DistanceSensor
from time import sleep
from threading import Thread


class DistanceSensorTest:
    def __init__(self, name, echo, trigger):
        self.__name = name
        self.__sensor = DistanceSensor(echo=echo, trigger=trigger, threshold_distance=0.1)
        self.__sensor.when_in_range = lambda: print(f'{name}: in range (callback)')
        self.__sensor.when_out_of_range = lambda: print(f'{name}: out of range (callback)')
        self.__printer_thread = None

    def print_distance(self, repeat_every=0):
        print(f'{self.__name}: at distance {self.__sensor.distance*100}cm')
        if repeat_every > 0:
            def loop_print():
                while self.__printer_thread is not None:
                    sleep(repeat_every)
                    print(f'{self.__name}: at distance {self.__sensor.distance*100}cm')

            old = self.__printer_thread
            self.__printer_thread = None
            old.join()
            self.__printer_thread = Thread(target=loop_print)
            self.__printer_thread.start()

    def check_in_range(self):
        if self.__sensor.value < self.__sensor.threshold:
            print(f'{self.__name}: already in range')
            return
        print(f'{self.__name}: now get in range')
        self.__sensor.wait_for_in_range()
        print(f'{self.__name}: correctly moved in range')

    def check_out_of_range(self):
        if self.__sensor.value > self.__sensor.threshold:
            print(f'{self.__name}: already out of range')
            return
        print(f'{self.__name}: now get out of range')
        self.__sensor.wait_for_out_of_range()
        print(f'{self.__name}: correctly moved out of range')


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
        
        
# Checks if all the sensors can be instantiated properly end starts printing status changes
front_sensor = FrontSensorTest()
back_sensor = BackSensorTest()
left_sensor = LeftSensorTest()
right_sensor = RightSensorTest()

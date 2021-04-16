import logging
from time import sleep

from gpiozero import DistanceSensor, Robot, LineSensor

from threading import Thread


class Movement:

    def __init__(self, standard_speed=0.25, avoidance_speed=0.25):
        # self.__sensorFront = DistanceSensor(echo=23, trigger=24, threshold_distance=0.1)
        # self.__sensorFront.when_in_range = self.__obstacle_front
        # self.__sensorFront.when_out_of_range = lambda: self.move_idle(2)

        # self.__sensorBack = DistanceSensor(echo=27, trigger=22, threshold_distance=0.1)
        # self.__sensorBack.when_in_range = self.__obstacle_back
        # self.__sensorBack.when_out_of_range = lambda: self.move_idle(2)

        self.__line_sensor = LineSensor(4)
        self.__line_sensor.when_line = self.__avoid_line

        self.__robot = Robot(left=(13, 19), right=(5, 6))

        self.__standard_speed = standard_speed
        self.__avoidance_speed = avoidance_speed

        self.__active = True

        def line_debug():
            while self.__active:
                sleep(0.3)
                print(self.__line_sensor.value)

        Thread(target=line_debug).start()

        logging.info('Robot initialized')

    def __avoid_line(self):
        print('Starting line avoidance routine')
        line = True
        def line_found():
            nonlocal line
            line = True
        self.__line_sensor.when_line = line_found
        self.__robot.backward(speed=self.__avoidance_speed, curve_left=1)
        print('waiting to lose line')
        while self.__line_sensor.value > 0.5:
            pass
        # self.__line_sensor.wait_for_no_line()
        sleep(1)
        print('waiting to see line again')
        while self.__line_sensor.value < 0.5:
            pass
        # self.__line_sensor.wait_for_line()
        print('resume movement')
        self.move_idle()
        print('waiting to leave line')
        while self.__line_sensor.value > 0.5:
            pass
        # self.__line_sensor.wait_for_no_line()
        print('re-enabling line avoidance callback')
        self.__line_sensor.when_line = self.__avoid_line
        print('Line avoidance finished')

    def __obstacle_front(self):
        logging.info('Avoiding obstacle on front')
        self.__robot.backward(speed=self.__avoidance_speed, curve_left=0.5)

    def __obstacle_back(self):
        logging.info('Avoiding obstacle on back')
        self.__robot.forward(speed=self.__avoidance_speed, curve_left=0.5)

    def move_idle(self, wait=0):
        sleep(wait)
        self.__robot.forward(speed=self.__standard_speed)

    def stop(self):
        self.__robot.stop()
        self.__active = False

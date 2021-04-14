import logging
from time import sleep

from gpiozero import DistanceSensor, Robot, LineSensor


class Movement:

    def __init__(self, standard_speed=0.25, avoidance_speed=0.25):
        self.__sensorFront = DistanceSensor(echo=23, trigger=24, threshold_distance=0.1)
        self.__sensorFront.when_in_range = self.__obstacle_front
        self.__sensorFront.when_out_of_range = lambda: self.move_idle(2)

        self.__sensorBack = DistanceSensor(echo=27, trigger=22, threshold_distance=0.1)
        self.__sensorBack.when_in_range = self.__obstacle_back
        self.__sensorBack.when_out_of_range = lambda: self.move_idle(2)

        self.__line_sensor = LineSensor(4, pull_up=True)
        self.__line_sensor.when_line = self.__avoid_line

        self.__robot = Robot(left=(13, 19), right=(5, 6))

        self.__standard_speed = standard_speed
        self.__avoidance_speed = avoidance_speed

        logging.info('Robot initialized')

    def __avoid_line(self):
        logging.info('Starting line avoidance routine')
        self.__line_sensor.when_line = None
        self.__robot.backward(speed=self.__avoidance_speed, curve_left=1)
        self.__line_sensor.wait_for_no_line()
        self.__line_sensor.wait_for_line()
        self.move_idle()
        self.__line_sensor.wait_for_no_line()
        self.__line_sensor.when_line = self.__avoid_line
        logging.info('Line avoidance finished')

    def __obstacle_front(self):
        logging.info('Avoiding obstacle on front')
        self.__robot.backward(speed=self.__avoidance_speed, curve_left=0.5)

    def __obstacle_back(self):
        logging.info('Avoiding obstacle on back')
        self.__robot.forward(speed=self.__avoidance_speed, curve_left=0.5)

    def move_idle(self, wait=0):
        sleep(wait)
        self.__robot.forward(speed=self.__standard_speed)

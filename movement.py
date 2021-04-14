import logging
from time import sleep

from gpiozero import DistanceSensor, Robot, LineSensor


class Movement:

    def __init__(self, standard_speed=0.25, avoidance_speed=0.25):
        self.__sensorFront = DistanceSensor(echo=23, trigger=24, threshold_distance=0.1)
        self.__sensorBack = DistanceSensor(echo=2, trigger=3, threshold_distance=0.1)
        self.__robot = Robot(left=(13, 19), right=(5, 6))
        self.__line_sensor = LineSensor(4, pull_up=True)
        self.__line_sensor.when_line = self.__avoid_line
        self.__sensorFront.when_deactivated = self.__obstacle_front
        self.__sensorBack.when_deactivated = self.__obstacle_back
        self.__standard_speed = standard_speed
        self.__avoidance_speed = avoidance_speed
        self.__sensorFront.when_activated = lambda: self.move_idle(2)
        self.__sensorBack.when_activated = lambda: self.move_idle(2)
        logging.info('Robot initialized')

    def __avoid_line(self):
        logging.info('Starting line avoidance routine')
        self.__robot.stop()
        self.__robot.backward(speed=self.__avoidance_speed, curve_left=1)
        self.__line_sensor.wait_for_active()
        self.__line_sensor.wait_for_inactive()
        self.move_idle()
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

from gpiozero import DistanceSensor, Robot, DigitalInputDevice
import logging


class Movement:

    def __init__(self):
        self.__sensorFront = DistanceSensor(echo=23, trigger=24, threshold_distance=0.1)
        self.__sensorBack = DistanceSensor(echo=2, trigger=3, threshold_distance=0.1)
        self.__robot = Robot(left=(13, 19), right=(5, 6))
        self.__line_sensor = DigitalInputDevice(4)
        self.__line_sensor.when_deactivated = self.__avoid_line
        self.__sensorFront.when_deactivated = self.__obstacle_front
        self.__sensorBack.when_deactivated = self.__obstacle_back
        logging.info('Robot initialized')

    def __avoid_line(self):
        logging.info('Starting line avoidance routine')
        self.__robot.stop()
        self.__robot.backward(speed=0.25, curve_left=1)
        self.__line_sensor.wait_for_active()
        self.__line_sensor.wait_for_inactive()
        self.__robot.stop()
        self.__robot.forward(speed=0.25)
        logging.info('Line avoidance finished')

    def __obstacle_front(self):
        logging.info('Avoiding obstacle on front')
        self.__robot.backward(speed=0.25, curve_left=0.5)

    def __obstacle_back(self):
        logging.info('Avoiding obstacle on back')
        self.__robot.forward(speed=0.25, curve_left=0.5)

    def move_idle(self):
        self.__robot.forward(speed=0.25)


movement = Movement

from gpiozero import DistanceSensor, Robot, DigitalInputDevice
import logging


class Movement:

    def __init__(self):
        self.__sensorFront = DistanceSensor(echo="BOARD10", trigger="", threshold_distance=0.1)
        self.__sensorBack = DistanceSensor(echo=18, trigger=17, threshold_distance=0.1)
        self.__robot = Robot(left=(4, 14), right=(17, 18))
        self.__line_sensor = DigitalInputDevice(9)
        self.__line_sensor.when_deactivated = self.__avoid_line
        self.__sensorFront.when_activated = self.__obstacle_front
        self.__sensorBack.when_activated = self.__obstacle_back
        self.__sensorFront.when_deactivated = self.__robot.stop
        self.__sensorBack.when_deactivated = self.__robot.stop
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
        self.__robot.stop()
        self.__robot.backward(speed=0.25)

    def __obstacle_back(self):
        logging.info('Avoiding obstacle on back')
        self.__robot.stop()
        self.__robot.forward(speed=0.25)

    def move_idle(self):
        self.__robot.stop()
        self.__robot.forward(speed=0.25)


movement = Movement

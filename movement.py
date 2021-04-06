from gpiozero import DistanceSensor, Robot, DigitalInputDevice
from time import sleep


class Movement:

    def __init__(self):
        self.__sensorFront = DistanceSensor(echo="BOARD10", trigger="", threshold_distance=0.1)
        self.__sensorBack = DistanceSensor(echo=18, trigger=17, threshold_distance=0.1)
        self.__robot = Robot(left=(4, 14), right=(17, 18))
        self.__line_sensor = DigitalInputDevice(9)
        self.__end_m = False
        self.__end_o = False

    def stop_robot(self):
        self.__end_m = True
        self.__end_o = True
        self.__robot.stop()

    def move_idle(self):

        while not self.__end_m:
            if self.__line_sensor.is_active:
                self.__robot.forward(speed=0.5)

            else:
                self.__robot.stop()
                self.__robot.backward(speed=0.5, curve_left=1)
                self.__line_sensor.wait_for_inactive()
                self.__robot.stop()
                self.__robot.forward(speed=0.5)
                self.__end_m = True

    def check_obstacles(self):

        while not self.__end_o:
            distance_front = self.__sensorFront.distance * 100
            distance_back = self.__sensorBack.distance * 100
            print("Distance front : %.1f" % distance_front)
            print("Distance back : %.1f" % distance_back)
            sleep(1)

            if distance_front <= 10:
                self.__robot.stop()
                self.__robot.backward(speed=0.5)
                distance_front.when_out_of_range = self.__robot.stop()
                self.__end_o = True

            if distance_back <= 10:
                self.__robot.stop()
                self.__robot.forward(speed=0.5)
                distance_back.when_out_of_range = self.__robot.stop()
                self.__end_o = True

movement = Movement
movement.move_idle()
movement.check_obstacles()
movement.stop_robot()

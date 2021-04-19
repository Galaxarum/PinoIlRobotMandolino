from time import sleep

from gpiozero import DistanceSensor, Robot, LineSensor
from face_tracking.face_detector_listener import FaceDetectorEventListener


class Movement(FaceDetectorEventListener):

    def __init__(self, standard_speed=0.25, avoidance_speed=0.25):
        self.__sensorFront = DistanceSensor(echo=23, trigger=24, threshold_distance=0.1)
        self.__sensorFront.when_in_range = self.__obstacle_front
        self.__sensorFront.when_out_of_range = lambda: self.move_idle(2)

        self.__sensorBack = DistanceSensor(echo=27, trigger=22, threshold_distance=0.1)
        self.__sensorBack.when_in_range = self.__obstacle_back
        self.__sensorBack.when_out_of_range = lambda: self.move_idle(2)

        self.__line_sensor = LineSensor(4, queue_len=10)
        self.__line_sensor.when_line = self.__avoid_line

        self.__robot = Robot(left=(13, 19), right=(5, 6))

        self.__standard_speed = standard_speed
        self.__avoidance_speed = avoidance_speed

        print('Robot initialized')

    def __avoid_line(self):
        print('Starting line avoidance routine')
        self.__robot.backward(speed=self.__avoidance_speed, curve_left=1)

        def on_leave_triggering_line():
            sleep(1)
            self.__line_sensor.when_line = on_line_again
            self.__line_sensor.when_no_line = None
            print('waiting to find line on back')

        def on_line_again():
            self.move_idle()
            sleep(1)
            self.__line_sensor.when_line = None
            self.__line_sensor.when_no_line = on_leave_ending_line
            print('waiting to leave line on back')

        def on_leave_ending_line():
            sleep(1)
            self.__line_sensor.when_line = self.__avoid_line
            self.__line_sensor.when_no_line = None
            print('Line avoidance finished')

        self.__line_sensor.when_line = None
        self.__line_sensor.when_no_line = on_leave_triggering_line
        print('waiting to leave triggering line')

    def __obstacle_front(self):
        print('Avoiding obstacle on front')
        self.__robot.backward(speed=self.__avoidance_speed, curve_left=0.5)

    def __obstacle_back(self):
        print('Avoiding obstacle on back')
        self.__robot.forward(speed=self.__avoidance_speed, curve_left=0.5)

    def on_valid_face_present(self, present):
        if present:
            pass
        else:
            self.move_idle()

    def on_face_position(self, position):
        if position == FaceDetectorEventListener.CENTER:
            self.__robot.forward(self.__standard_speed)
        elif position == FaceDetectorEventListener.LEFT:
            self.__robot.left(self.__standard_speed)
        elif position == FaceDetectorEventListener.RIGHT:
            self.__robot.right(self.__standard_speed)
        else:
            raise ValueError(f'Unexpected face position: {position}')

    def move_idle(self, wait=0):
        print('Moving')
        sleep(wait)
        self.__robot.forward(speed=self.__standard_speed)

    def stop(self):
        self.__robot.stop()

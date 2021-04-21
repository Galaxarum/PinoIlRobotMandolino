import atexit
import logging
from time import sleep

from gpiozero import DistanceSensor, Robot, LineSensor

from face_detection import FaceDetectorEventListener


class Movement(FaceDetectorEventListener):

    def __init__(self, standard_speed=0.25, avoidance_speed=0.25):
        self.__sensorFront = DistanceSensor(echo=24, trigger=25, threshold_distance=0.1)
        self.__sensorFront.when_in_range = self.__obstacle_front

        self.__sensorBack = DistanceSensor(echo=27, trigger=22, threshold_distance=0.1)
        self.__sensorBack.when_in_range = self.__obstacle_back

        self.__line_sensor = LineSensor(4, queue_len=10)
        self.__line_sensor.when_line = self.__avoid_line

        self.__robot = Robot(left=(13, 26), right=(5, 6))

        self.__standard_speed = standard_speed
        self.__avoidance_speed = avoidance_speed

        atexit.register(lambda: self.__robot.close())
        atexit.register(lambda: self.__sensorBack.close())
        atexit.register(lambda: self.__sensorFront.close())
        atexit.register(lambda: self.__line_sensor.close())

        self.__log = logging.getLogger('movement')
        self.__log.info('Movement initialized')

        self.move_idle()

    def __stop_avoiding(self):
        self.__sensorFront.when_out_of_range = None
        self.__sensorBack.when_out_of_range = None
        self.__line_sensor.when_line = self.__avoid_line
        self.__line_sensor.when_no_line = None

    def __avoid_line(self):
        return   # todo: re-enable me
        print('Starting line avoidance routine')
        self.__robot.backward(speed=self.__avoidance_speed, curve_left=1)
        self.__sensorFront.when_in_range = None

        def on_leave_triggering_line():
            sleep(1)
            self.__line_sensor.when_line = on_line_again
            self.__line_sensor.when_no_line = None
            print('waiting to find line on back')

        def on_line_again():    # todo: critical case of obstacle in front when leaving second line
            self.__robot.forward(speed=self.__avoidance_speed)
            self.__sensorFront.when_in_range = self.__obstacle_front
            self.__sensorBack.when_in_range = None
            sleep(1)
            self.__line_sensor.when_line = None
            self.__line_sensor.when_no_line = on_leave_ending_line
            print('waiting to leave line on back')

        def on_leave_ending_line():
            self.__line_sensor.when_line = self.__avoid_line
            self.__line_sensor.when_no_line = None
            self.__sensorBack.when_in_range = self.__obstacle_back
            print('Line avoidance finished')

        # todo: critical case of obstacle on back when leaving first line
        self.__line_sensor.when_line = None
        self.__line_sensor.when_no_line = on_leave_triggering_line
        print('waiting to leave triggering line')

    def __obstacle_front(self):
        def on_avoiding_ended():
            self.__sensorFront.when_out_of_range = None
            self.move_idle(2)
        self.__stop_avoiding()
        self.__log.info('Avoiding obstacle on front')
        self.__robot.backward(speed=self.__avoidance_speed, curve_left=0.5)
        # todo: what if i find a line when going back?
        self.__sensorFront.when_out_of_range = on_avoiding_ended

    def __obstacle_back(self):
        def on_avoiding_ended():
            self.__sensorBack.when_out_of_range = None
            self.move_idle(2)
        self.__stop_avoiding()
        self.__log.info('Avoiding obstacle on back')
        self.__robot.forward(speed=self.__avoidance_speed, curve_left=0.5)
        self.__sensorBack.when_out_of_range = on_avoiding_ended

    def __avoiding(self):
        return self.__sensorFront.when_out_of_range is not None \
               or self.__sensorBack.when_out_of_range is not None \
               or self.__line_sensor.when_line == self.__avoid_line

    def on_valid_face_present(self, present):
        if not self.__avoiding():
            if present:
                pass
            else:
                #self.move_idle()
                pass

    def on_face_position(self, position):
        if not self.__avoiding():
            if position == FaceDetectorEventListener.CENTER:
                self.__robot.forward(self.__standard_speed)
                self.__log.info('approaching person in front')
            elif position == FaceDetectorEventListener.LEFT:
                self.__robot.right(self.__standard_speed)    # left e right sono invertiti per qualche motivo
                self.__log.info('turning left')
            elif position == FaceDetectorEventListener.RIGHT:
                self.__robot.left(self.__standard_speed)    # left e right sono invertiti per qualche motivo
                self.__log.info('turning right')
            else:
                raise ValueError(f'Unexpected face position: {position}')

    def move_idle(self, wait=0):
        self.__log.info('rotating forever (idle)')
        sleep(wait)
        self.__robot.right(speed=self.__standard_speed)

    def stop(self):
        self.__stop_avoiding()
        self.__robot.stop()


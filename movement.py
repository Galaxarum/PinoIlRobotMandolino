import atexit
import logging
from time import sleep

from gpiozero import DistanceSensor, Robot, LineSensor

from face_detection import FaceDetectorEventListener


class Movement(FaceDetectorEventListener):

    def __init__(self, standard_speed=0.25, avoidance_speed=0.25):
        self.__sensorFront = DistanceSensor(echo=24, trigger=25, threshold_distance=0.2)
        self.__sensorBack = DistanceSensor(echo=27, trigger=22, threshold_distance=0.2)
        self.__line_sensor = LineSensor(4, queue_len=10)

        self.__robot = Robot(left=(13, 26), right=(5, 6))

        self.__standard_speed = standard_speed
        self.__avoidance_speed = avoidance_speed

        atexit.register(lambda: self.__robot.close())
        atexit.register(lambda: self.__sensorBack.close())
        atexit.register(lambda: self.__sensorFront.close())
        atexit.register(lambda: self.__line_sensor.close())

        self.__log = logging.getLogger('movement')

        self.__reset_avoidances()
        self.move_idle()

        self.__log.info('Movement initialized')

    def __reset_avoidances(self):
        self.__sensorFront.when_in_range = self.__obstacle_front
        self.__sensorFront.when_out_of_range = None

        self.__sensorBack.when_in_range = self.__obstacle_back
        self.__sensorBack.when_out_of_range = None

        self.__line_sensor.when_line = self.__avoid_line
        self.__line_sensor.when_no_line = None

    def __avoid_line(self):
        def on_leave_triggering_line():
            self.__line_sensor.when_line = on_line_again
            self.__line_sensor.when_no_line = None

            sleep(1)
            self.__log.info('waiting to find line on back')

        def on_line_again():
            def conflict_obstacle_front():
                self.stop()
                # resume line routine from here when obstacle removed
                self.__sensorFront.when_out_of_range = on_line_again

            # if obstacle prevents from leaving the line, wait
            self.__sensorFront.when_in_range = conflict_obstacle_front

            self.__sensorBack.when_in_range = None  # ignore back obstacles when moving forward

            self.__line_sensor.when_line = None
            self.__line_sensor.when_no_line = on_leave_ending_line

            self.__robot.forward(speed=self.__avoidance_speed)
            self.__log.info('waiting to leave line on back')

        def on_leave_ending_line():
            self.move_idle(2)
            self.__reset_avoidances()
            self.__log.info('Line avoidance finished')

        self.__log.info('Starting line avoidance routine')
        self.__reset_avoidances()

        self.__sensorFront.when_in_range = None     # ignore front obstacles while moving back

        def conflict_obstacle_back():
            self.stop()
            # resume line routine from here when obstacle removed
            self.__sensorBack.when_out_of_range = self.__avoid_line

        self.__line_sensor.when_line = None
        self.__line_sensor.when_no_line = on_leave_triggering_line

        self.__sensorBack.when_in_range = conflict_obstacle_back    # if obstacle prevents from leaving the line, wait

        self.__robot.backward(speed=self.__avoidance_speed, curve_left=1)
        self.__log.info('waiting to leave triggering line')

    def __obstacle_front(self):
        def on_avoiding_ended():
            self.__sensorFront.when_out_of_range = None
            self.__line_sensor.when_line = self.__avoid_line
            self.move_idle(2)

        self.__reset_avoidances()
        self.__log.info('Avoiding obstacle on front')
        self.__robot.backward(speed=self.__avoidance_speed, curve_left=0.5)
        # if a line is found when going back, stop. out of range will remain active, allowing to restart movement
        self.__line_sensor.when_line = self.stop
        self.__sensorFront.when_out_of_range = on_avoiding_ended

    def __obstacle_back(self):
        def on_avoiding_ended():
            self.__sensorBack.when_out_of_range = None
            self.move_idle(2)

        self.__reset_avoidances()
        self.__log.info('Avoiding obstacle on back')
        self.__robot.forward(speed=self.__avoidance_speed, curve_left=0.5)
        self.__sensorBack.when_out_of_range = on_avoiding_ended

    def __avoiding(self):

        return self.__sensorFront.when_out_of_range is not None \
               or self.__sensorBack.when_out_of_range is not None \
               or self.__line_sensor.when_line != self.__avoid_line

    def on_valid_face_present(self, present, distance):

        if distance == FaceDetectorEventListener.NEAR:
            self.__sensorFront.when_on_range = None
            self.__sensorBack.when_on_range = None
            self.__line_sensor.when_line = None
            self.__robot.stop()

    def on_face_position(self, position):
        self.__log.debug('on face position')
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

    def on_face_leaving(self):
        self.__reset_avoidances()
        self.move_idle()

    def move_idle(self, wait=0):
        self.__log.info('rotating forever (idle)')
        sleep(wait)
        self.__robot.forward(speed=self.__standard_speed, curve_right=0.5)
        # self.__robot.right(speed=self.__standard_speed)

    def stop(self):
        self.__robot.stop()


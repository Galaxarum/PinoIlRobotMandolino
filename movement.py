from time import sleep

from gpiozero import DistanceSensor, Robot, LineSensor
from face_detection import FaceDetectorEventListener, FaceDetector
import logging
import sys
import atexit


# --- CONST ---

FILE_PATH = {
    'FACE_SAMPLES_FILE': 'haarcascade_frontalface_alt.xml'
}
EXIT_CHAR = 'e'
WAITING_INTERVAL = 40 # milliseconds
CAM_RES_WIDTH = 320
CAM_RES_HEIGHT = 240
DEFAULT_CAMERA_DEVICE = 0
MIRROR_CAMERA = False

# --- FUNCTIONS ---


def print_init_info():
    print('INITIALIZATION INFO')
    print('{')
    print('Samples files: ')
    for key, value in FILE_PATH.items():
        print(') {0} -> {1}'.format(key, value))
    print('Exit Char:', EXIT_CHAR)
    print('Interval between captures (milliseconds):', WAITING_INTERVAL)
    print('Cam width:', CAM_RES_WIDTH)
    print('Cam height:', CAM_RES_HEIGHT)
    print('Default Camera Device:', DEFAULT_CAMERA_DEVICE)
    print('}')


class Movement(FaceDetectorEventListener):

    def __init__(self, standard_speed=0.25, avoidance_speed=0.25):
        self.__sensorFront = DistanceSensor(echo=24, trigger=25, threshold_distance=0.1)
        self.__sensorFront.when_in_range = self.__obstacle_front
        self.__sensorFront.when_out_of_range = lambda: self.move_idle(2)

        self.__sensorBack = DistanceSensor(echo=27, trigger=22, threshold_distance=0.1)
        self.__sensorBack.when_in_range = self.__obstacle_back
        self.__sensorBack.when_out_of_range = lambda: self.move_idle(2)

        self.__line_sensor = LineSensor(4, queue_len=10)
        self.__line_sensor.when_line = self.__avoid_line

        self.__robot = Robot(left=(13, 26), right=(5, 6))

        self.__standard_speed = standard_speed
        self.__avoidance_speed = avoidance_speed

        atexit.register(lambda: self.__robot.close())
        atexit.register(lambda: self.__sensorBack.close())
        atexit.register(lambda: self.__sensorFront.close())
        atexit.register(lambda: self.__line_sensor.close())

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
            print('approaching person in front')
        elif position == FaceDetectorEventListener.LEFT:
            self.__robot.left(self.__standard_speed)
            print('turning left')
        elif position == FaceDetectorEventListener.RIGHT:
            self.__robot.right(self.__standard_speed)
            print('turning right')
        else:
            raise ValueError(f'Unexpected face position: {position}')

    def move_idle(self, wait=0):
        print('rotating forever (idle)')
        sleep(wait)
        self.__robot.right(speed=self.__standard_speed)

    def stop(self):
        self.__robot.stop()


if __name__ == '__main__':
    #test_listener = Listener()
    m = Movement()
    face_detector = FaceDetector(FILE_PATH, EXIT_CHAR, WAITING_INTERVAL, DEFAULT_CAMERA_DEVICE, CAM_RES_WIDTH, CAM_RES_HEIGHT, MIRROR_CAMERA)

    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    print_init_info()

    face_detector.add_event_listener(m)
    face_detector.start_detection()

    print('Terminated')

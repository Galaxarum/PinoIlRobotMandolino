from gpiozero import DistanceSensor
from face_detection import FaceDetector
from movement import Movement
from game import Game
from game_inside import GameMuseumDefinitive
from time import sleep
from speech import TTS
import logging
import sys
import os

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

# --- GLOBAL VAR ---
triggered_sensor = None

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


def sensor_left_triggered():
    global triggered_sensor
    triggered_sensor = 'left'
    print('Main: left triggered')


def sensor_right_triggered():
    global triggered_sensor
    triggered_sensor = 'right'
    print('Main: right triggered')


if __name__ == '__main__':
    sensorLeft = DistanceSensor(echo=17, trigger=23, threshold_distance=0.03)
    sensorRight = DistanceSensor(echo=7, trigger=9, threshold_distance=0.03)
    startup_commands = []

    sensorRight.when_in_range = sensor_right_triggered
    sensorLeft.when_in_range = sensor_left_triggered

    tts = TTS()

    tts.say('Put your feet under the left gear to start the internal game. Put your feet under the right sensor to start the external game')

    # Wait for one of left/right sensor to be triggered
    while triggered_sensor is None:
        print('Left distance', sensorLeft.distance)
        print('Right distance', sensorRight.distance)
        sleep(0.05)

    # Selection of game
    if triggered_sensor == 'right':
        # Outside
        #startup_commands = ['movement', 'outside', 'face']
        print('right: selected game outside')
    elif triggered_sensor == 'left':
        # Inside
        #startup_commands = ['inside']
        print('left: selected game inside')

    # Closing of side sensors
    sensorLeft.close()
    sensorRight.close()

    # ------------------------------------------ like old main

    face_detector = FaceDetector(FILE_PATH, EXIT_CHAR, WAITING_INTERVAL, DEFAULT_CAMERA_DEVICE, CAM_RES_WIDTH,
                                 CAM_RES_HEIGHT, MIRROR_CAMERA)

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # Movement initializing section
    if 'movement' in startup_commands:
        print('movement enabled')
        m = Movement(standard_speed=0.5, avoidance_speed=0.5)
        face_detector.add_event_listener(m)

    game = None
    # Game initializing section
    if 'outside' in startup_commands:
        os.system("amixer sset 'Headphone' 100%")
        print('game outside enabled')
        game = Game()
        face_detector.add_event_listener(game)

    elif 'inside' in startup_commands:
        os.system("amixer sset 'Headphone' 93%")
        print('game inside enabled')
        game = GameMuseumDefinitive()
        game.start_game()

    # Face recognition activation
    if 'face' in startup_commands:
        print('face enabled')
        print_init_info()
        face_detector.start()
        face_detector.join()

    # Keep shell opened
    command = input()
    while command != 'stop':
        command = input()
    if game is not None:
        game.close()

    print('Terminated')

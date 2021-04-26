from face_detection import FaceDetector
from movement import Movement
from game import Game
from game_museum import GameMuseum
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


#todo use sensors to select game mode
if __name__ == '__main__':
    face_detector = FaceDetector(FILE_PATH, EXIT_CHAR, WAITING_INTERVAL, DEFAULT_CAMERA_DEVICE, CAM_RES_WIDTH,
                                 CAM_RES_HEIGHT, MIRROR_CAMERA)

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # Movement initializing section
    if 'movement' in sys.argv:
        print('movement enabled')
        m = Movement(standard_speed=0.5, avoidance_speed=0.5)
        face_detector.add_event_listener(m)

    game = None
    # Game initializing section
    if 'outside' in sys.argv:
        os.system("amixer sset 'Headphone' 100%")
        print('game outside enabled')
        game = Game()
        game.start()
    elif 'inside' in sys.argv:
        os.system("amixer sset 'Headphone' 93%")
        print('game inside enabled')
        game = GameMuseum()
        game.start()

    if game is not None:
        command = input()
        while command != 'stop':
            command = input()

        game.set_continue_play(False)
        game.join()

    if 'face' in sys.argv:
        print('face enabled')
        print_init_info()
        face_detector.start()
        face_detector.join()

    print('Terminated')

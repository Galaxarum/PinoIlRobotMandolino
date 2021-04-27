from face_detection import FaceDetector
from movement import Movement
from game import Game
from game_inside import GameMuseumDefinitive
from answer_passing import AnswerReceiver
import logging
import sys
import os

# --- CONST ---

FILE_PATH = {
    'FACE_SAMPLES_FILE': 'haarcascade_frontalface_alt.xml'
}
EXIT_CHAR = 'e'
WAITING_INTERVAL = 40  # milliseconds
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


if __name__ == '__main__':
    face_detector = FaceDetector(FILE_PATH, EXIT_CHAR, WAITING_INTERVAL, DEFAULT_CAMERA_DEVICE, CAM_RES_WIDTH,
                                 CAM_RES_HEIGHT, MIRROR_CAMERA)

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    game_selector = AnswerReceiver()
    while game_selector.get_answer() is None:
        # todo: use a tts to ask for game mode
        game_selector.query_answer(('outside', 'inside'), timeout=5)    # todo: ask again for game mode

    game_mode = game_selector.get_answer()
    game_selector.close()

    if game_mode == 'outside':
        os.system("amixer sset 'Headphone' 100%")
        print('game outside enabled')
        game = Game()
        game.start()

    elif game_mode == 'inside':
        os.system("amixer sset 'Headphone' 93%")
        print('game inside enabled')
        game = GameMuseumDefinitive()
        game.start_game()

    print('movement enabled')
    m = Movement(standard_speed=0.5, avoidance_speed=0.5)
    face_detector.add_event_listener(m)

    print('face enabled')
    print_init_info()
    face_detector.start()
    face_detector.join()

    # terminated by shutting down

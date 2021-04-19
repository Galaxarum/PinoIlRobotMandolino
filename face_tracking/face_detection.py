from face_detector import FaceDetector
from face_detector_listener import FaceDetectorEventListener
import logging
import sys

# --- CONST ---

FILE_PATH = {
    'FACE_SAMPLES_FILE': 'haarcascade_frontalface_alt.xml'
}
EXIT_CHAR = 'e'
WAITING_INTERVAL = 40 # milliseconds
CAM_RES_WIDTH = 640
CAM_RES_HEIGHT = 480
DEFAULT_CAMERA_DEVICE = 0

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

# TEST CLASS


class Listener(FaceDetectorEventListener):

    def __init__(self):
        super().__init__()

    def on_valid_face_present(self, present):
        """
        Override
        """
        print('Valid face present:', present)

    def on_face_position(self, position):
        """
        Override
        """
        print('Face position changed:', position)


# --- MAIN ---

if __name__ == '__main__':
    test_listener = Listener()
    face_detector = FaceDetector(FILE_PATH, EXIT_CHAR, WAITING_INTERVAL, DEFAULT_CAMERA_DEVICE, CAM_RES_WIDTH, CAM_RES_HEIGHT)

    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    print_init_info()

    face_detector.add_event_listener(test_listener)
    face_detector.start_detection()

    print('Terminated')

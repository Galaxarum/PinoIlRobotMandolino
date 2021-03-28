from face_detector import FaceDetector
import logging
import sys

# --- CONST ---

FILE_PATH = {
    'FACE_SAMPLES_FILE': 'haarcascade_frontalface_alt.xml'
}
EXIT_CHAR = 'e'
WAITING_INTERVAL = 40 # milliseconds
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
    print('Default Camera Device:', DEFAULT_CAMERA_DEVICE)
    print('}')

# --- MAIN ---

if __name__ == '__main__':
    face_detector = FaceDetector(FILE_PATH, EXIT_CHAR, WAITING_INTERVAL, DEFAULT_CAMERA_DEVICE)

    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    print_init_info()

    face_detector.start_detection()

    print('Terminated')

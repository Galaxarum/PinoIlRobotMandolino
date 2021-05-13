# Related OpenCV Tutorial: https://docs.opencv.org/4.5.1/db/d28/tutorial_cascade_classifier.html
#
# Related github link of haarcascades: https://github.com/opencv/opencv/tree/master/data/haarcascades OR...
# ...in case OpenCV is installed with Anaconda3 in home dir: /home/<user>/anaconda3/share/opencv4/haarcascades

from __future__ import print_function
import cv2 as cv
from threading import Thread
import math
import logging
from time import time


# TEST CLASS


class FaceDetectorEventListener:
    CENTER = 'center'
    RIGHT = 'right'
    LEFT = 'left'
    FAR = 'far'
    MIDDLE = 'middle'
    NEAR = 'near'

    def on_valid_face_present(self, present, distance):
        """
        Called when a face is being detected for a certain amount of time.
        """
        pass

    def on_face_position(self, position):
        """
        Called when a face <change> position in the camera window.
        <change> := if a face stay in a specified part of the screen the method is NOT called. It's called
        only if the face switch from a section to another.

        Arguments:
             position: Position of the face in the camera window
             distance: xyz
        """
        pass

    def on_face_leaving(self):
        pass


class Listener(FaceDetectorEventListener):

    def __init__(self):
        super().__init__()

    def on_valid_face_present(self, present, distance):
        """
        Override
        """
        # print('Valid face present:', present, 'and it\'s', distance)

    def on_face_position(self, position):
        """
        Override
        """
        print('Face position changed:', position)

    def on_face_leaving(self):
        print('Persona andata via')


class FaceDetector(Thread):

    def __init__(self, file_path, exit_char, waiting_interval, default_camera_device, cam_res_width, cam_res_height,
                 mirror_camera=False, debug=False):
        super().__init__()

        # (Private)
        self.__file_path = file_path
        self.__exit_char = exit_char
        self.__waiting_interval = waiting_interval
        self.__default_camera_device = default_camera_device
        self.__cam_res_width = cam_res_width
        self.__cam_res_height = cam_res_height
        self.__mirror_camera = mirror_camera

        self.__face_cascade_classifier = None
        self.__color = (255, 0, 0)
        self.__event_listeners = []

        self.__face_timer = None

        self.__frame_division = 3  # ! WARNING: This value is hardcoded since the code is developed on that value.
        self.__frame_width_block = cam_res_width // self.__frame_division
        self.__center_side_frame_offset = 15

        self.__current_face_position = FaceDetectorEventListener.CENTER
        self.__is_face_present = False

        self.__face_area_FAR = range(0, 1200)
        self.__face_area_MIDDLE = range(1200, 2300)
        self.__face_area_NEAR = range(2300, 60000)
        self.__current_face_distance = FaceDetectorEventListener.MIDDLE

        self.__log = logging.getLogger('face detection')
        if debug:
            self.add_event_listener(Listener())

    def run(self):
        self.start_detection()

    def __on_valid_face_present(self):
        for event_listener in self.__event_listeners:
            event_listener.on_valid_face_present(self.__is_face_present, self.__current_face_distance)

    def __on_face_position(self):
        if self.__mirror_camera:
            if self.__current_face_position == FaceDetectorEventListener.RIGHT:
                self.__current_face_position = FaceDetectorEventListener.LEFT
            elif self.__current_face_position == FaceDetectorEventListener.LEFT:
                self.__current_face_position = FaceDetectorEventListener.RIGHT

        for event_listener in self.__event_listeners:
            event_listener.on_face_position(self.__current_face_position)

    def __on_face_leaving(self):
        for event_listener in self.__event_listeners:
            event_listener.on_face_leaving()

    def __detect_face(self, frame):
        """
        Identify faces in a frame using Haar method and relative samples.

        Arguments:
            frame: The frame used to perform face detection

        Return:
            The frame with faces bounds
        """
        biggest_face = None

        frame_gray_scale = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame_gray_scale_equalized = cv.equalizeHist(frame_gray_scale)

        faces = self.__face_cascade_classifier.detectMultiScale(frame_gray_scale_equalized)

        if len(faces) > 0:
            self.__face_timer = time() # Previous->None; Now-> seconds
            biggest_face = faces[0]

            # Find the biggest face
            for (x, y, width, height) in faces:
                if width > biggest_face[2] and height > biggest_face[3]:
                    biggest_face = (x, y, width, height)

            # Draw the biggest face over the frame
            biggest_face_x = biggest_face[0]
            biggest_face_y = biggest_face[1]
            biggest_face_width = biggest_face[2]
            biggest_face_height = biggest_face[3]

            center = (biggest_face_x + biggest_face_width // 2, biggest_face_y + biggest_face_height // 2)
            area = (biggest_face_height // 2) * (biggest_face_width // 2) * math.pi  # ellipse area
            area = math.floor(area)

            frame = cv.ellipse(frame, center,
                               (biggest_face_width // 2, biggest_face_height // 2),
                               0, 0, 360, self.__color, 4)

            # Find, basing on the face center, the portion of the frame in which the face is contained.
            # If the position is different from the previous one, an event is thrown.
            if center[0] in range(0, self.__frame_width_block + self.__center_side_frame_offset):
                self.__log.debug('face left')
                if self.__current_face_position != FaceDetectorEventListener.LEFT:
                    self.__current_face_position = FaceDetectorEventListener.LEFT
                    self.__on_face_position()
            elif center[0] in range(self.__frame_width_block + self.__center_side_frame_offset, (2 * self.__frame_width_block) - self.__center_side_frame_offset):
                self.__log.debug('face center')
                if self.__current_face_position != FaceDetectorEventListener.CENTER:
                    self.__current_face_position = FaceDetectorEventListener.CENTER
                    self.__on_face_position()
            elif center[0] in range((2 * self.__frame_width_block) - self.__center_side_frame_offset, (3 * self.__frame_width_block)):
                self.__log.debug('face right')
                if self.__current_face_position != FaceDetectorEventListener.RIGHT:
                    self.__current_face_position = FaceDetectorEventListener.RIGHT
                    self.__on_face_position()

            # Find, basing on the area, the distance of the face
            if area in self.__face_area_FAR:
                self.__current_face_distance = FaceDetectorEventListener.FAR
            elif area in self.__face_area_MIDDLE:
                self.__current_face_distance = FaceDetectorEventListener.MIDDLE
            elif area in self.__face_area_NEAR:
                self.__current_face_distance = FaceDetectorEventListener.NEAR

            print('Face area:', area)

            # Signal that a face has been recognized, MUST be called after calculation of the face area
            self.__is_face_present = True
            self.__on_valid_face_present()
        else:
            # Face not present

            if self.__face_timer is not None:  # In this way event generation is stopped if a face is continuosly not detected
                if time() - self.__face_timer > 5:
                    self.__on_face_leaving()
                    self.__face_timer = None

            self.__is_face_present = False
            self.__on_valid_face_present()

        return frame

    def start_detection(self):
        """
        Begin detection of faces

        ! This is a blocking method
        """
        face_cascade_file_name = self.__file_path['FACE_SAMPLES_FILE']
        self.__face_cascade_classifier = cv.CascadeClassifier()
        camera_device = None
        capture = None

        self.__log.debug('Loading samples...')

        if not self.__face_cascade_classifier.load(cv.samples.findFile(face_cascade_file_name)):
            print('Samples loading error')
            exit(0)

        self.__log.debug('Loading samples OK')

        camera_device = self.__default_camera_device
        capture = cv.VideoCapture(camera_device)
        capture.set(cv.CAP_PROP_FRAME_WIDTH, self.__cam_res_width)
        capture.set(cv.CAP_PROP_FRAME_HEIGHT, self.__cam_res_height)

        self.__log.debug('Check image capturing...')

        if not capture.isOpened():
            print('Video Capture error')
            exit(0)

        self.__log.debug('Check image capturing OK')

        while True:
            return_value, frame = capture.read()

            if frame is None:
                print('No captured frame')
                break

            frame_with_detection = self.__detect_face(frame)
            cv.imshow('Face detection', frame_with_detection)
            #cv.imshow('Face detection', frame)

            if (cv.waitKey(self.__waiting_interval) == ord(self.__exit_char)):
                break

    def add_event_listener(self, event_listener):
        self.__event_listeners.append(event_listener)


if __name__ == '__main__':
    # decommentare imshow quando si fa il test
    FILE_PATH = {
        'FACE_SAMPLES_FILE': 'haarcascade_frontalface_alt.xml'
    }
    EXIT_CHAR = 'e'
    WAITING_INTERVAL = 40  # milliseconds
    CAM_RES_WIDTH = 320
    CAM_RES_HEIGHT = 240
    DEFAULT_CAMERA_DEVICE = 0
    MIRROR_CAMERA = False

    listener = Listener()
    face_detector = FaceDetector(FILE_PATH, EXIT_CHAR, WAITING_INTERVAL, DEFAULT_CAMERA_DEVICE, CAM_RES_WIDTH,
                                 CAM_RES_HEIGHT, MIRROR_CAMERA)

    face_detector.add_event_listener(listener)

    face_detector.start()
    face_detector.join()

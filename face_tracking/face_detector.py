# Related OpenCV Tutorial: https://docs.opencv.org/4.5.1/db/d28/tutorial_cascade_classifier.html
#
# Related github link of haarcascades: https://github.com/opencv/opencv/tree/master/data/haarcascades OR...
# ...in case OpenCV is installed with Anaconda3 in home dir: /home/<user>/anaconda3/share/opencv4/haarcascades

from __future__ import print_function
import cv2 as cv
import logging
import sys

class FaceDetector:

    def __init__(self, file_path, exit_char, waiting_interval, default_camera_device, cam_res_width, cam_res_height):
        # (Private)
        self.__file_path = file_path
        self.__exit_char = exit_char
        self.__waiting_interval = waiting_interval
        self.__default_camera_device = default_camera_device
        self.__cam_res_width = cam_res_width
        self.__cam_res_height = cam_res_height
        self.__face_cascade_classifier = None
        self.__color = (255, 0, 0)

    def __detect_face(self, frame):
        """
        Identify faces in a frame using Haar method and relative samples. 

        Arguments:
            frame: The frame used to perform face detection 

        Return:
            The frame with faces bounds
        """
        frame_gray_scale = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame_gray_scale_equalized = cv.equalizeHist(frame_gray_scale)

        faces = self.__face_cascade_classifier.detectMultiScale(frame_gray_scale_equalized)

        for (x, y, width, height) in faces:
            center = (x + width // 2, y + height // 2)

            frame = cv.ellipse(frame, center, (width // 2, height // 2), 0, 0, 360, self.__color, 4)

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

        logging.debug('Loading samples...')

        if not self.__face_cascade_classifier.load(cv.samples.findFile(face_cascade_file_name)):
            print('Samples loading error')
            exit(0)

        logging.debug('Loading samples OK')

        camera_device = self.__default_camera_device
        capture = cv.VideoCapture(camera_device)
        capture.set(cv.CAP_PROP_FRAME_WIDTH, 640)
        capture.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

        logging.debug('Check image capturing...')

        if not capture.isOpened():
            print('Video Capture error')
            exit(0)
        
        logging.debug('Check image capturing OK')

        while True:
            return_value, frame = capture.read()

            if frame is None:
                print('No captured frame')
                break
            
            frame_with_detection = self.__detect_face(frame)
            cv.imshow('Face detection', frame_with_detection)
            # cv.imshow('Face detection', frame)

            if (cv.waitKey(self.__waiting_interval) == ord(self.__exit_char)):
                break

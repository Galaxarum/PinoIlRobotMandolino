from gpiozero import DistanceSensor
from speech import TTS
from time import sleep
from led_matrices import LedMatrices
import os
import random


class GameMuseumDefinitive:

    def __init__(self):
        # Available instruments with relative sound files to be played
        # ! At least one instrument MUST be inserted
        self.__available_instruments = {
            'guitar': ['guitar_1.mp3'],
            'violin': ['violin_1.mp3'],
        }
        self.__current_instrument_id = 0

        # Phrases that the robot can play
        self.__random_phrases = ['I suggest you to visit all the rooms!', 'Look at these beautiful instruments!']

        self.__threshold_distance = 0.03
        # Confirm instrument
        self.__sensorLeft = DistanceSensor(echo=17, trigger=23, queue_len=1, threshold_distance=0.03)
        self.__sensorLeft.when_in_range = self.__test_trigger
        # Change instrument
        self.__sensorRight = DistanceSensor(echo=7, trigger=9, queue_len=1, threshold_distance=0.03)
        self.__sensorRight.when_in_range = self.__test_trigger

        self.__left_distance = 1
        self.__right_distance = 1

        # (Not used alternative)
        # What to do when a foot is near the sensor: change instrument
        #self.__sensorRight.when_in_range = self.__change_instrument

        self.__tts = TTS()
        self.__emotion_controller = LedMatrices()

    def __test_trigger(self):
        self.__left_distance = self.__sensorLeft.distance
        self.__right_distance = self.__sensorRight.distance
        #print('right triggered:', self.__sensorRight.distance)

    # (Eventually triggered by an event, but not in our case)
    def __change_instrument(self):
        # Choose next instrument
        if self.__current_instrument_id + 1 < len(self.__available_instruments.keys()):
            self.__current_instrument_id = self.__current_instrument_id + 1
        else:
            self.__current_instrument_id = 0

        # Tell the user the new selected instrument
        new_phrase = 'Now you have selected ' + list(self.__available_instruments.keys())[self.__current_instrument_id]
        self.__say(new_phrase)

    def __say(self, text):
        self.__tts.say(text, blocking=True)
        #print(text)

    def start_game(self):
        # Show a type of eye
        self.__emotion_controller.eye_neutral()
        
        # Tell user to chose the instrument that he wants to play and to confirm his choice
        self.__say('Use left foot to change instrument and right foot to confirm')

        # Main loop
        while True:
            # Wait for an answer by the user, checking manually thresholds
            # (while both aren't seeing obstacles do nothing)
            self.__left_distance = 1
            self.__right_distance = 1
            #print('Left distance:', left_distance)
            #print('Right distance:', right_distance)
            while self.__left_distance > self.__threshold_distance and self.__right_distance > self.__threshold_distance:
                # Wait for 50 milliseconds
                sleep(0.05)
                # Reassign new values
                #left_distance = self.__sensorLeft.distance
                #print('Left distance:', left_distance)
                #right_distance = self.__sensorRight.distance
                #print('Right distance:', right_distance)

            # As soon as an event occurs we check which of the two sensors has been triggered, checking saved values

            # Left (confirm) sensor activated
            if self.__left_distance <= self.__threshold_distance:
                # Instrument is confirmed! We exit from the main loop and start to play sounds!
                print('[Internal Game] Confirmed instrument')
                break
            # Right (change inst.) sensor activated
            elif self.__right_distance <= self.__threshold_distance:
                print('[Internal Game] Change instrument')
                self.__change_instrument()
            else:
                print('[Internal Game] Something wrong with sensors...')

        # Out of the main loop, we play sounds of the selected instrument

        # Get a list of mp3 (value of the selected instrument key)
        music_file_list = list(self.__available_instruments.values())[self.__current_instrument_id]
    
        self.__emotion_controller.eye_sad()
    
        for music_file in music_file_list:
            # Play music file (BLOCKING os call)
            os.system('mpg123 ' + 'sounds/internal_game/' + music_file)
            # Say something randomly
            self.__emotion_controller.eye_neutral() # sad, bored, angry
            self.__say(random.sample(self.__random_phrases, 1)[0])
            self.__emotion_controller.eye_sad()


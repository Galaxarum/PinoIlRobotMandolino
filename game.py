import os
from feet_answer import FeetAnswer
from time import time


class Game:

    NO_GAME_TIMEOUT = 10  # s
    REPEAT_ANSWER_TIMEOUT = 20  # s

    def __init__(self, sensor_left, sensor_right, time_before_exit, speech_object, emotion_controller):
        self.__sensor_right = sensor_right
        self.__sensor_left = sensor_left
        self.__time_before_exit = time_before_exit
        self.__speech_object = speech_object
        self.__emotion_controller = emotion_controller
        self.__feet_receiver = FeetAnswer(self)
        self.__answer = None

        self.__sound = {
            'one': 'sound1.mp3',
            'two': 'sound2.mp3'
        }

    def start(self):

        self.__say('hello! do you want to play a game?')

        #sensor eneble to receive an answer
        # if no signal in a slot of time -> exit
        # else set answer
        self.__feet_receiver.restart_routine()

        timeout = time()
        while self.__answer is None and time()-timeout < Game.NO_GAME_TIMEOUT:
            pass

        if self.__answer is None or not self.__answer:
            return

        self.__say('Ok! I will play two sounds, than you can answer')

        self.__say('Sound number 1')
        self.__play_sound('one')
        self.__say('Sound number 2')
        self.__play_sound('two')

        self.__say('Put you feet on left sensor to answer 1')
        self.__say('Put you feet on rigth sensor to answer 2')

        #sensor enable to receive an answer
        # if no signal in a slot of time -> exit
        # else set answer
        self.__feet_receiver.restart_routine()
        timeout = time()
        while self.__answer is None:
            if time()-timeout < Game.REPEAT_ANSWER_TIMEOUT:     # repeat answer on timeout
                self.__say('Ok! I will play two sounds, than you can answer')

                self.__say('Sound number 1')
                self.__play_sound('one')
                self.__say('Sound number 2')
                self.__play_sound('two')

                timeout = time()

        if self.__answer:
            #self._show_emotion('happy')
            self.__say('Right!')

        else:
            #self._show_emotion('sad')
            self.__say('Oh no! you loose')

    def __say(self, text):
        # say text, call external class
        pass

    def __play_sound(self, sound_code):
        os.system('mpg123 ' + self.__sound[sound_code])

    def __show_emotion(self, emotion_string):
        if self.__emotion_controller is not None:
            self.__emotion_controller.show_emotion(emotion_string)

    def receive_answer(self, answer):
        self.__answer = answer

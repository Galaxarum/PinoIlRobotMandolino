from random import Random
from time import time
from time import sleep

from feet_answer import FeetAnswer
from led_matrices import LedMatrices
from speech import SpeechRecognizer, TTS


class Game:

    NO_GAME_TIMEOUT = 10  # s
    REPEAT_ANSWER_TIMEOUT = 20  # s

    def __init__(self):
        self.__speech_recognizer = SpeechRecognizer()
        self.__emotion_controller = LedMatrices()
        self.__speech_object = TTS(mouth_controller=self.__emotion_controller)
        self.__feet_receiver = FeetAnswer(self)
        self.__answer = None
        self.__random = Random()

        self.__sound = {
            'one': 'sound1.mp3',
            'two': 'sound2.mp3'
        }

    def start(self):

        self.__say('hello! do you want to play a game?')

        #sensor eneble to receive an answer
        # if no signal in a slot of time -> exit
        # else set answer
        self.__get_answer(Game.NO_GAME_TIMEOUT)

        if self.__answer is None or not self.__answer:
            return
        self.__answer = None

        self.__say('Ok! I will play two sounds, than you can answer')

        self.__say('Sound number 1')
        self.__say('one')
        self.__say('Sound number 2')
        self.__say('two')

        self.__say('Put you feet on left sensor to answer 1')
        self.__say('Put you feet on rigth sensor to answer 2')

        #sensor enable to receive an answer
        # if no signal in a slot of time -> exit
        # else set answer

        def on_timeout():
            self.__say('Ok! I will play two sounds, than you can answer')

            self.__say('Sound number 1')
            self.__say('one')
            self.__say('Sound number 2')
            self.__say('two')

            return True

        self.__get_answer(Game.REPEAT_ANSWER_TIMEOUT, on_timeout)

        if self.__answer is not None:
            if self.__answer:
                self.__show_emotion(False)
                self.__say('Right!')
            else:
                self.__show_emotion(True)
                self.__say('Oh no! you lost')

    def __say(self, text):
        self.__speech_object.say(text, blocking=True)
        print(text)

    def __show_emotion(self, real_emotion):
        if self.__emotion_controller is not None:
            if real_emotion:
                rand = self.__random.randint(1,3)
                if rand == 1:
                    self.__emotion_controller.eye_sad()
                elif rand == 2:
                    self.__emotion_controller.eye_bored()
                elif rand == 3:
                    self.__emotion_controller.eye_angry()
            else:
                self.__emotion_controller.eye_neutral()

    def __get_answer(self, timeout, on_timeout=None):
        """

        :param timeout: the maximum time to wait for an answer
        :param on_timeout: A function to execute on timeout. If it returns true, the timeout will be restarted, otherwise (false, no value returned, null function) it will stop waiting for an answer
        """
        self.__feet_receiver.restart_routine()
        #self.__speech_recognizer.listen_and_recognize(self)

        start_time = time()
        while self.__answer is None:
            if time() - start_time < timeout:
                sleep(0.1)
                print('time tick...')
            elif on_timeout is not None and on_timeout():
                self.__get_answer(timeout, on_timeout)
            else:
                return

    def receive_answer(self, answer):
        if self.__answer is None:
            self.__answer = answer

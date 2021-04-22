from random import Random
from time import time
from time import sleep

from feet_answer import FeetAnswer
from led_matrices import LedMatrices
from speech import SpeechRecognizer, TTS
from tests.game_test import GameTest


class Game:

    QUESTIONS_PER_GAME = 3
    MAX_QUESTION_REPETITIONS = 3
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

        game_handler = GameTest()
        self.__say('hello! do you want to play a game?')

        # sensor enable to receive an answer
        # if no signal in a slot of time -> exit
        # else set answer

        self.__get_answer(Game.NO_GAME_TIMEOUT, [True, False])

        if self.__answer is None or not self.__answer:
            return
        self.__answer = None

        self.__say('Ok! Lets start the game')
        self.__say('Put you feet on the right sensor to choose the first answer')
        self.__say('Put you feet on the left sensor to choose the second answer')

        def question_timeout(question_tuple):
            nonlocal repeated_times
            repeated_times += 1
            if repeated_times < Game.MAX_QUESTION_REPETITIONS:
                self.__say_question(question_tuple)
                return True
            else:
                return False

        for i in range(Game.QUESTIONS_PER_GAME):
            element = game_handler.retrieve_element()
            self.__say_question(element)
            repeated_times = 0

            # sensor enable to receive an answer
            # if no signal in a slot of time -> exit
            # else set answer

            self.__get_answer(Game.REPEAT_ANSWER_TIMEOUT, element[1:], on_timeout=lambda: question_timeout(element))

            if self.__answer is None:   # Passed maximum repetitions
                return
            else:
                checked_answer = game_handler.check_answer(element[0], self.__answer)

                if checked_answer:
                    self.__show_emotion(sad_emotion=False)
                    self.__say('Right!')
                else:
                    self.__show_emotion(sad_emotion=True)
                    self.__say('Oh no! you lost')

                self.__answer = None

        self.__say('I thank you to have participated to this game')
        self.__say('Come to the Musical Instruments Museum to learn more')

    def __say_question(self, question_tuple):
        self.__say(question_tuple[0])
        self.__say(question_tuple[1])
        self.__say(question_tuple[2])

    def __say(self, text):
        self.__speech_object.say(text, blocking=True)
        print(text)

    def __show_emotion(self, sad_emotion):
        if self.__emotion_controller is not None:
            if sad_emotion:
                rand = self.__random.randint(1, 3)
                if rand == 1:
                    self.__emotion_controller.eye_sad(60)
                elif rand == 2:
                    self.__emotion_controller.eye_bored()
                elif rand == 3:
                    self.__emotion_controller.eye_angry()
            else:
                self.__emotion_controller.eye_neutral()

    def __get_answer(self, timeout, answers, on_timeout=None):
        """

        :param timeout: the maximum time to wait for an answer
        :param on_timeout: A function to execute on timeout. If it returns true, the timeout will be restarted, otherwise (false, no value returned, null function) it will stop waiting for an answer
        """
        self.__feet_receiver.restart_routine(answers[0], answers[1])
        self.__speech_recognizer.listen_and_recognize(self)

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
            self.__feet_receiver.end_routine()

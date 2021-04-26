from random import Random
from time import time
from time import sleep

from answer_passing import AnswerReceiver
from feet_answer import FeetAnswer
from led_matrices import LedMatrices
from speech import SpeechRecognizer, TTS
from game_test import GameTest
from face_detection import FaceDetectorEventListener


class Game(AnswerReceiver, FaceDetectorEventListener):

    QUESTIONS_PER_GAME = 3
    MAX_QUESTION_REPETITIONS = 3
    NO_GAME_TIMEOUT = 10  # s
    REPEAT_ANSWER_TIMEOUT = 20  # s
    INTER_ANSWER = ['Next question is', 'Another one now', 'Lets move on']
    POS_FEEDBACK = ['Well done', 'Right', 'Good job']
    NEG_FEEDBACK = ['Oh nooo']

    def __init__(self):
        self.__speech_recognizer = SpeechRecognizer(self)
        self.__emotion_controller = LedMatrices()
        self.__speech_object = TTS(mouth_controller=self.__emotion_controller)
        self.__feet_receiver = FeetAnswer(self)
        self.__answer = None
        self.__random = Random()
        self.running = False

    def start(self):
        self.running = True

        try:
            game_handler = GameTest()
            self.__say('hello! do you want to play a game?')

            # sensor enable to receive an answer
            # if no signal in a slot of time -> exit
            # else set answer

            self.__get_answer(Game.NO_GAME_TIMEOUT, [True, False])

            if self.__answer is None or not self.__answer:
                self.__end_game_sad()
                return
            self.__answer = None

            self.__say('Ok! Lets start the game')
            self.__say('I\'m gonna ask you some questions, can you help me find the answers?')

            self.__say('Put your feet in front of the gear on your left to choose the first answer')
            self.__say('Put your feet in front of the gear on your right to choose the second answer')

            self.__say('Otherwise, you can say first or second to choose your answer')

            def question_timeout(question_tuple):
                nonlocal repeated_times
                repeated_times += 1
                if repeated_times < Game.MAX_QUESTION_REPETITIONS:
                    self.__say_question(question_tuple)
                    return True
                else:
                    return False

            for i in range(Game.QUESTIONS_PER_GAME):
                self.__emotion_controller.eye_neutral()
                element = game_handler.retrieve_element()
                if i == 0:
                    self.__say('The first question is')
                elif i == Game.QUESTIONS_PER_GAME - 1:
                    s = self.__random.sample(Game.INTER_ANSWER, 1)[0]
                    self.__say(s)
                else:
                    self.__say('Almost there, last question!')

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
                        s = self.__random.sample(Game.POS_FEEDBACK, 1)[0]
                        self.__say(s)
                    else:
                        self.__show_emotion(sad_emotion=True)
                        s = self.__random.sample(Game.NEG_FEEDBACK, 1)[0]
                        self.__say(s)

                    self.__answer = None

            self.__say('thank you for playing this game')
            self.__say('Come to the Musical Instruments Museum to learn more')
        except ValueError:
            self.__end_game_sad()
            return

    def __end_game_sad(self):
        self.__emotion_controller.eye_sad()
        self.__say('I\'m sorry you don\'t want to play with me')

    def __say_question(self, question_tuple):
        self.__say(question_tuple[0])
        self.__say(question_tuple[1])
        self.__say(question_tuple[2])

    def __say(self, text):
        if self.running:
            self.__speech_object.say(text, blocking=True)
            print(text)
        else:
            raise ValueError('Game not running')

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
        self.__feet_receiver.provide_answer(answers[0], answers[1])
        self.__speech_recognizer.provide_answer(answers[0], answers[1])

        start_time = time()
        while self.__answer is None:
            if time() - start_time < timeout:
                sleep(0.1)
            elif on_timeout is not None and on_timeout():
                self.__get_answer(timeout, answers, on_timeout=on_timeout)
            else:
                return

    def receive_answer(self, answer):
        if self.__answer is None:
            self.__answer = answer
            self.__feet_receiver.stop()

    def on_face_leaving(self):
        self.running = False

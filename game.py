from random import Random
from time import time
from time import sleep

from answer_passing import AnswerReceiver
from led_matrices import LedMatrices
from speech import TTS
from game_test import GameTest
from face_detection import FaceDetectorEventListener


class Game(AnswerReceiver, FaceDetectorEventListener):

    QUESTIONS_PER_GAME = 3
    MAX_QUESTION_REPETITIONS = 3
    NO_GAME_TIMEOUT = 10  # s
    REPEAT_ANSWER_TIMEOUT = 20  # s
    INTER_ANSWER = ['Next question is.mp3', 'Another one now.mp3', 'Let\'s move on.mp3']
    POS_FEEDBACK = ['Well done.mp3', 'Right.mp3', 'Good job.mp3']
    NEG_FEEDBACK = ['Oh no.mp3']

    def __init__(self):
        super().__init__()
        self.__emotion_controller = LedMatrices()
        self.__speech_object = TTS(mouth_controller=self.__emotion_controller)
        self.__random = Random()
        self.running = False

    def start(self):
        self.running = True

        try:
            game_handler = GameTest()
            self.__say('Hello.mp3')
            self.__say('Do you want to play a game.mp3')

            # sensor enable to receive an answer
            # if no signal in a slot of time -> exit
            # else set answer

            self.query_answer([True, False], Game.NO_GAME_TIMEOUT)
            print(self._answer)

            if self._answer is None or not self._answer:
                self.__end_game_sad()
                return
            self._answer = None

            self.__say('Let\'s start the game.mp3')
            self.__say('I\'m gonna ask you some quesitons.mp3')
            self.__say('I\'m gonna ask you some questions.mp3')
            # self.__say('can you help me find the answers?')

            self.__say('Feet gear left.mp3')
            self.__say('Feet gear right.mp3')

            self.__say('You can say first or second.mp3')

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
                    self.__say('The first question is.mp3')
                elif i == Game.QUESTIONS_PER_GAME - 1:
                    s = self.__random.sample(Game.INTER_ANSWER, 1)[0]
                    self.__say(s)
                else:
                    self.__say('Last quesiton.mp3')

                self.__say_question(element)
                repeated_times = 0

                # sensor enable to receive an answer
                # if no signal in a slot of time -> exit
                # else set answer

                self.query_answer(element[1:], Game.REPEAT_ANSWER_TIMEOUT, on_timeout=lambda: question_timeout(element))

                if self._answer is None:   # Passed maximum repetitions
                    return
                else:
                    checked_answer = game_handler.check_answer(element[0], self._answer)

                    if checked_answer:
                        self.__show_emotion(sad_emotion=False)
                        s = self.__random.sample(Game.POS_FEEDBACK, 1)[0]
                        self.__say(s)
                    else:
                        self.__show_emotion(sad_emotion=True)
                        s = self.__random.sample(Game.NEG_FEEDBACK, 1)[0]
                        self.__say(s)

                    self._answer = None

            self.__say('Thank you for playing.mp3')
            self.__say('Come to the museum.mp3')
        except ValueError:
            self.__end_game_sad()
            return

    def __end_game_sad(self):
        self.__emotion_controller.eye_sad()
        self.__say('I\'m sorry you don\'t want to play.mp3')

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

    def on_valid_face_present(self, present, distance):
        if self.running == False and distance == FaceDetectorEventListener.NEAR:
            print('STARTING GAME FROM EVENT')
            self.start()

    def on_face_leaving(self):
        self.running = False

    def close(self):
        super(Game, self).close()
        self.running = False

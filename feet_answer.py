from gpiozero import DistanceSensor
from game import Game


class FeetAnswer:

    def __init__(self, game):
        self.__game = game
        self.__sensorLeft = DistanceSensor(echo=25, trigger=8, threshold_distance=0.3)
        self.__sensorRight = DistanceSensor(echo=10, trigger=9, threshold_distance=0.3)
        self.__end = False
        self.__sensorLeft.when_in_range = self.__left_answer
        self.__sensorRight.when_in_range = self.__right_answer
        self.__sensorLeft.when_out_of_range = self.__end_routine
        self.__sensorRight.when_out_of_range = self.__end_routine

    def __end_routine(self):
        print('ending')
        self.__end = True

    def enable(self):
        self.__end = False

    def __left_answer(self):
        if not self.__end:
            #self.game.receiveAnswer(True)
            print("Correct answer")

    def __right_answer(self):
        if not self.__end:
            #self.game.receiveAnswer(False)
            print("Wrong answer")

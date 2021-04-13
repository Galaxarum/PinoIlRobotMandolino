from gpiozero import DistanceSensor
from game import Game


class FeetAnswer:

    def __init__(self, game):
        self.game = game
        self.sensorLeft = DistanceSensor(echo=25, trigger=8, threshold_distance=0.1)
        self.sensorRight = DistanceSensor(echo=27, trigger=22, threshold_distance=0.1)
        self.end = False
        self.sensorLeft.when_activated = self.__left_answer
        self.sensorRight.when_activated = self.__right_answer
        self.sensorLeft.when_deactivated = self.__end_routine
        self.sensorRight.when_deactivated = self.__end_routine

    def __end_routine(self):
        self.end = True

    def __left_answer(self):
        if not self.end:
            self.game.receiveAnswer(True)

    def __right_answer(self):
        if not self.end:
            self.game.receiveAnswer(False)

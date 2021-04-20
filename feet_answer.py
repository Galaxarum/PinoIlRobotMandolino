from gpiozero import DistanceSensor
import atexit


class FeetAnswer:

    def __init__(self, game):
        self.__game = game
        self.__sensorLeft = DistanceSensor(echo=17, trigger=23, threshold_distance=0.4)
        self.__sensorRight = DistanceSensor(echo=7, trigger=9, threshold_distance=0.4)
        self.__disabled = True
        self.__sensorLeft.when_in_range = self.__left_answer
        self.__sensorRight.when_in_range = self.__right_answer

        atexit.register(lambda: self.__sensorRight.close())
        atexit.register(lambda: self.__sensorLeft.close())

    def __end_routine(self):
        self.__disabled = True

    def restart_routine(self):
        self.__disabled = False
        print('Sensors disabled')

    def __left_answer(self):
        print('left')
        if not self.__disabled:
            print("True answer")
            self.__game.receive_answer(True)
            self.__end_routine()

    def __right_answer(self):
        if not self.__disabled:
            print("False answer")
            self.__game.receive_answer(False)
            self.__end_routine()

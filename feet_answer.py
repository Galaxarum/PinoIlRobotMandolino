from gpiozero import DistanceSensor
import pyttsx3


class FeetAnswer:

    def __init__(self):
        self.engine = pyttsx3.init()
        self.sensorLeft = DistanceSensor(echo=21, trigger=20, threshold_distance=0.1)
        self.sensorRight = DistanceSensor(echo=18, trigger=17, threshold_distance=0.1)
        self.end = False
        self.sensorLeft.when_activated = self.__left_answer
        self.sensorRight.when_activated = self.__right_answer
        self.sensorLeft.when_deactivated = self.__end_routine
        self.sensorRight.when_deactivated = self.__end_routine

    def __end_routine(self):
        self.end = True

    def __left_answer(self):
        if not self.end:
            self.engine.say('Correct answer')
            self.engine.runAndWait()

    def __right_answer(self):
        if not self.end:
            self.engine.say('Wrong answer')
            self.engine.runAndWait()

from gpiozero import DistanceSensor
import atexit

import answer_passing


class FeetAnswer(answer_passing.AnswerProvider):

    def __init__(self, answer_receiver: answer_passing.AnswerReceiver):
        super().__init__(answer_receiver)
        self.__sensorLeft = DistanceSensor(echo=17, trigger=23, threshold_distance=0.4)
        self.__sensorRight = DistanceSensor(echo=7, trigger=9, threshold_distance=0.4)
        self.__disabled = True
        self.__left_ans = None
        self.__right_ans = None
        self.__sensorLeft.when_in_range = self.__left_answer
        self.__sensorRight.when_in_range = self.__right_answer

        atexit.register(lambda: self.__sensorRight.close())
        atexit.register(lambda: self.__sensorLeft.close())

    def stop(self):
        self.__disabled = True

    def provide_answer(self, first_answer, second_answer):
        self.__disabled = False
        self.__left_ans = second_answer
        self.__right_ans = first_answer
        print('Sensors disabled')

    def __left_answer(self):
        if not self.__disabled:
            print("Left answer")
            self._answer_receiver.receive_answer(self.__left_ans)

    def __right_answer(self):
        if not self.__disabled:
            print("Right answer")
            self._answer_receiver.receive_answer(self.__right_ans)

    def close(self):
        self.__sensorLeft.close()
        self.__sensorRight.close()

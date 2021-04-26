from time import time, sleep

from feet_answer import FeetAnswer
from speech import SpeechRecognizer


class AnswerReceiver:
    def __init__(self):
        self._answer = None
        self.__feet_answer = FeetAnswer(self)
        self.__speech = SpeechRecognizer(self)

    def query_answer(self, answers, timeout, on_timeout=None):
        """
                :param answers: a tuple of answers to expect, in order
                :param timeout: the maximum time to wait for an answer
                :param on_timeout: A function to execute on timeout. If it returns true, the timeout will be restarted, otherwise (false, no value returned, null function) it will stop waiting for an answer
                """
        self.__feet_answer.provide_answer(answers[0], answers[1])
        self.__speech.provide_answer(answers[0], answers[1])

        start_time = time()
        while self._answer is None:
            if time() - start_time < timeout:
                sleep(0.1)
            elif on_timeout is not None and on_timeout():
                self.query_answer(timeout, answers, on_timeout=on_timeout)
            else:
                return

    def receive_answer(self, answer):
        if self._answer is not None:
            self._answer = answer
            self.__feet_answer.stop()

    def close(self):
        self.__feet_answer.close()


class AnswerProvider:
    def __init__(self, answer_receiver: AnswerReceiver):
        self._answer_receiver = answer_receiver

    def provide_answer(self, first_answer, second_answer):
        raise SystemError('not implemented')

    def stop(self):
        pass

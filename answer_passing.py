from time import time, sleep
from gpiozero import DistanceSensor
import atexit
from threading import Thread

import speech_recognition as sr


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
        if self._answer is None:
            self._answer = answer
            self.__feet_answer.stop()

    def close(self):
        self.__feet_answer.close()

    def get_answer(self):
        return self._answer


class AnswerProvider:
    def __init__(self, answer_receiver: AnswerReceiver):
        self._answer_receiver = answer_receiver

    def provide_answer(self, first_answer, second_answer):
        raise SystemError('not implemented')

    def stop(self):
        pass


class SpeechRecognizer(AnswerProvider):

    def __init__(self, answer_receiver: AnswerReceiver, lang='en-US'):
        super().__init__(answer_receiver)
        self.lang = lang
        self.__recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            self.__recognizer.adjust_for_ambient_noise(mic, 5)

    def get_audio(self) -> sr.AudioData:
        with sr.Microphone() as mic:
            print("Listening for audio")
            return self.__recognizer.record(mic, duration=5)

    def recognize(self, audio: sr.AudioData) -> str:
        result = None

        # fallback to google speech recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            result = self.__recognizer.recognize_google(audio, language=self.lang)
            print("Google Speech Recognition thinks you said ", result)
            return result
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as ex:
            print("Could not request results from Google Speech Recognition service", ex)

        try:
            result = self.__recognizer.recognize_sphinx(audio, language=self.lang)
            print("Sphinx thinks you said ", result)
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as ex:
            print("Sphinx error", ex)

        return result

    def provide_answer(self, first_answer, second_answer):
        def underlying_function():
            audio = self.get_audio()
            print('acquired audio')
            answer = self.recognize(audio)
            if answer is None:
                return
            answer = answer.lower()
            answer_reported = None

            if 'first' in answer or 'yes' in answer or 'left' in answer:
                answer_reported = first_answer

            if 'second' in answer or 'no' in answer or 'right' in answer:
                answer_reported = second_answer

            if answer_reported is not None:
                self._answer_receiver.receive_answer(answer_reported)

        Thread(name='Answer recognizer', target=underlying_function).start()


class FeetAnswer(AnswerProvider):

    def __init__(self, answer_receiver: AnswerReceiver):
        super().__init__(answer_receiver)
        self.__DEFAULT_ANSWER_DISTANCE = 0.12
        self.__sensorLeft = DistanceSensor(echo=17, trigger=23, threshold_distance=self.__DEFAULT_ANSWER_DISTANCE, partial=True)
        self.__sensorRight = DistanceSensor(echo=7, trigger=9, threshold_distance=self.__DEFAULT_ANSWER_DISTANCE, partial=True)
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

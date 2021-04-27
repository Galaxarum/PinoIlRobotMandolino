import os
from threading import Thread

import speech_recognition as sr
from gtts import gTTS

import answer_passing


class SpeechRecognizer(answer_passing.AnswerProvider):

    def __init__(self, answer_receiver: answer_passing.AnswerReceiver, lang='en-US'):
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


class TTS:
    __TTS_FILE = 'temp_tts_out.ogg'

    def __init__(self, lang='en', mouth_controller=None):
        self.lang = lang
        self.__mouth_controller = mouth_controller
        self.__busy_observer = None

    def __say_blocking(self, text):
        tts = gTTS(text=text, lang=self.lang)
        tts.save(TTS.__TTS_FILE)
        self.__play_file_blocking(TTS.__TTS_FILE)
        os.remove(TTS.__TTS_FILE)

    def __play_file_blocking(self, filename):
        if self.__mouth_controller is not None:
            self.__mouth_controller.speak()
        os.system(f'mpg123 -q {filename}')
        if self.__mouth_controller is not None:
            self.__mouth_controller.stop_speak()

    def say(self, text, blocking=False):
        def player():
            file_path = os.path.join('sounds', text)

            if os.path.isfile(file_path):
                self.__play_file_blocking(file_path)
            else:
                self.__say_blocking(text)
        if blocking:
            player()
        else:
            Thread(target=player, name='Audio Player').start()


if __name__ == '__main__':
    t = TTS()
    t.say('Ciao sono un tts')

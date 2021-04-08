import threading

import speech_recognition as sr
from gtts import gTTS
import pygame
import os


class SpeechRecognizer:

    def __init__(self, lang='it-IT'):
        self.lang = lang
        self.__recognizer = sr.Recognizer()
        self.__GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""INSERT THE CONTENTS OF THE GOOGLE CLOUD SPEECH JSON CREDENTIALS FILE HERE"""
        # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
        self.__IBM_USERNAME = "INSERT IBM SPEECH TO TEXT USERNAME HERE"
        # IBM Speech to Text passwords are mixed-case alphanumeric strings
        self.__IBM_PASSWORD = "INSERT IBM SPEECH TO TEXT PASSWORD HERE"

    def get_audio(self):
        with sr.Microphone() as mic:
            print("Listening for audio")
            return self.__recognizer.listen(mic, timeout=5)

    def recognize(self, audio):
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

        if result is not None:
            return result
        # fallback to google cloud
        try:
            result = self.__recognizer.recognize_google_cloud(audio, language=self.lang,
                                                              credentials_json=self.__GOOGLE_CLOUD_SPEECH_CREDENTIALS)
            print("Google Cloud Speech thinks you said ", result)
        except sr.UnknownValueError:
            print("Google Cloud Speech could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Cloud Speech service; {0}".format(e))

        if result is not None:
            return result
        # recognize speech using IBM Speech to Text
        try:
            result = self.__recognizer.recognize_ibm(audio, language=self.lang,
                                                     username=self.__IBM_USERNAME, password=self.__IBM_PASSWORD)
            print("IBM Speech to Text thinks you said " + result)
        except sr.UnknownValueError:
            print("IBM Speech to Text could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from IBM Speech to Text service; {0}".format(e))

        if result is not None:
            return result

        try:
            result = self.__recognizer.recognize_sphinx(audio, language=self.lang)
            print("Sphinx thinks you said ", result)
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as ex:
            print("Sphinx error", ex)

        return result

    def listen_and_recognize(self):
        audio = self.get_audio()
        print('acquired audio')
        return self.recognize(audio)


class TTS:
    __TTS_FILE = 'temp_tts_out.mp3'

    def __init__(self, lang='it'):
        self.lang = lang
        pygame.mixer.init()

    def __say_blocking(self, text):
        while pygame.mixer.music.get_busy():
            continue
        tts = gTTS(text=text, lang=self.lang)
        tts.save(TTS.__TTS_FILE)
        pygame.mixer.music.load(TTS.__TTS_FILE)
        pygame.mixer.music.play()
        os.remove(TTS.__TTS_FILE)

    def say(self, text):
        threading.Thread(target=lambda: self.__say_blocking(text))


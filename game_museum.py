import atexit

from speech import TTS
from threading import Thread

#todo fix me

class GameMuseum(Thread):

    def __init__(self):
        super().__init__()

        self.__tts_object = TTS()

        self.__available_sounds = {
            'violin' : 'violin.mp3',
            'cetra' : 'cetra.mp3',
        }
        self.__continue_play = True

    def run(self) -> None:
        while self.__continue_play:
            self.__play_sound()

    def set_continue_play(self, set_value) -> None:
        self.__continue_play = set_value

    def __play_sound(self) -> None:
        # Play all sounds in the dictionary
        for key in self.__available_sounds.keys():
            self.__tts_object.say(self.__available_sounds[key], blocking=True)

import os
from threading import Thread

from gtts import gTTS


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
        os.system(f'mpg123 -q "{filename}"')
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

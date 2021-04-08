import os

class Game:

    def __init__(self, sensor_left, sensor_rigth, time_before_exit, speech_object, emotion_controller):
        self._sensor_rigth = sensor_rigth
        self._sensor_left = sensor_left
        self._time_before_exit = time_before_exit
        self._speech_object = speech_object
        self._emotion_controller = emotion_controller

        self._sound = {
            'one': 'sound1.mp3',
            'two': 'sound2.mp3'
        }

    def start(self):
        answer = None

        self._say('hello! do you want to play a game?')

        #sensor eneble to receive an answer
        # if no signal in a slot of time -> exit
        # else set answer

        self._say('Ok! I will play two sounds, than you can answer')

        self._say('Sound number 1')
        self._play_sound('one')
        self._say('Sound number 2')
        self._play_sound('two')

        self._say('Put you feet on left sensor to answer 1')
        self._say('Put you feet on rigth sensor to answer 2')

        #sensor eneble to receive an answer
        # if no signal in a slot of time -> exit
        # else set answer

        if answer == 'left':
            #self._show_emotion('happy')
            self._say('Rigth!')
        elif answer == 'rigth':
            #self._show_emotion('sad')
            self._say('Oh no! you loose')
            

    def _say(self, text):
        # say text, call external class
        pass

    def _play_sound(self, sound_code):
        os.system('mpg123 ' + self._sound[sound_code])


    def _show_emotion(self, emotion_string):
        if self._emotion_controller is not None:
            self._emotion_controller.show_emotion(emotion_string)
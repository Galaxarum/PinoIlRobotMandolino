import os

class Game:

    def __init__(self, sensor_left, sensor_rigth, time_before_exit, speech_object, emotion_controller):
        self.__sensor_rigth = sensor_rigth
        self.__sensor_left = sensor_left
        self.__time_before_exit = time_before_exit
        self.__speech_object = speech_object
        self.__emotion_controller = emotion_controller

        self.__sound = {
            'one': 'sound1.mp3',
            'two': 'sound2.mp3'
        }

    def start(self):
        answer = None

        self.__say('hello! do you want to play a game?')

        #sensor eneble to receive an answer
        # if no signal in a slot of time -> exit
        # else set answer

        self.__say('Ok! I will play two sounds, than you can answer')

        self.__say('Sound number 1')
        self.__play_sound('one')
        self.__say('Sound number 2')
        self.__play_sound('two')

        self.__say('Put you feet on left sensor to answer 1')
        self.__say('Put you feet on rigth sensor to answer 2')

        #sensor eneble to receive an answer
        # if no signal in a slot of time -> exit
        # else set answer

        if answer == 'left':
            #self._show_emotion('happy')
            self.__say('Rigth!')
        elif answer == 'rigth':
            #self._show_emotion('sad')
            self.__say('Oh no! you loose')
            

    def __say(self, text):
        # say text, call external class
        pass

    def __play_sound(self, sound_code):
        os.system('mpg123 ' + self.__sound[sound_code])


    def __show_emotion(self, emotion_string):
        if self.__emotion_controller is not None:
            self.__emotion_controller.show_emotion(emotion_string)
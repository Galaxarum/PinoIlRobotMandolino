import random


class GameTest:

    game_elements = [["How many chords a bass.mp3", "Four.mp3", "Five.mp3"],
                     ["Where is located the museum.mp3", "At the triennale.mp3", "At the triennale-2.mp3"],
                     ["The musical staff.mp3", "True.mp3", "False.mp3"],
                     ["The violin was invented.mp3", "False.mp3", "True.mp3"],
                     ["Vivaldi Priest.mp3", "True.mp3", "False.mp3"],
                     ["Musical phonology.mp3", "True.mp3", "False.mp3"],
                     ["First core 50s.mp3", "False.mp3", "True.mp3"],
                     ["Age oldest instrument.mp3", "More 100 ys.mp3", "Less 100ys.mp3"],
                     ["Which kind of instrument i remind.mp3", "Guitar.mp3", "Violin.mp3"],
                     ["What do you expect to find.mp3", "Only instruments.mp3", "Instruments and documents.mp3"]]

    def __init__(self):

        random.shuffle(GameTest.game_elements)
        self.__chosen = GameTest.game_elements[:3].copy()
        self.__answer = None
        self.__index = 0

    def retrieve_element(self):
        element = self.__chosen[self.__index]
        self.__index = self.__index + 1
        if random.randint(1, 2) == 2:
            t = element[1]
            element[1] = element[2]
            element[2] = t
        return element

    def check_answer(self, question, answer):

        for game_tuple in GameTest.game_elements:
            q = game_tuple[0]
            if q == question:
                return game_tuple[1] == answer
            else:
                continue

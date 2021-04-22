import random


class GameTest:

    game_elements = [["How many chords a bass guitar have?", "four", "five"],
                     ["Where is located the Musical Instruments Museum in Milan?", "Inside the Castello Sforzesco", "At the Triennale"],
                     ["The musical staff has five lines and four spaces", "True", "False"],
                     ["The violin was invented in fifteenth century", "False", "True"],
                     ["Antonio Vivaldi was a priest", "True", "False"],
                     ["The Musical Instruments Museum hosts a reconstruction of the Study of Musical Phonology", "True", "False"],
                     ["The first core of the Musical Instruments Museum was set up in the Fifties", "False", "True"],
                     ["What is the age of the oldest instrument here?", "more than one hundred years", "max one hundred years"],
                     ["Which kind of instrument I remember to you", "Guitar", "Violin"],
                     ["What do you expect to find in the museum?", "Only instruments", "Instruments and musical material like documents, sheets"]]

    def __init__(self):

        random.shuffle(GameTest.game_elements)
        self.__chosen = GameTest.game_elements[:3]
        self.__answer = None
        self.__index = 0
        for c in self.__chosen:
            rand = random.randint(1, 2)
            if rand == 2:
                temp = c[1]
                c[1] = c[2]
                c[2] = temp

    def retrieve_element(self):

        element = self.__chosen[self.__index]
        self.__index = self.__index + 1
        return element

    def check_answer(self, question, answer):

        for game_tuple in GameTest.game_elements:
            q = game_tuple[0]
            if q == question:
                return game_tuple[1] == answer
            else:
                continue

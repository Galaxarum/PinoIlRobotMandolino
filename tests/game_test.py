import random


class GameTest:

    game_elements = [["How many chords a bass guitar have?", "four", "five"],
               ["Where is located the Musical Instruments Museum in Milan?", "Inside the Castello Sforzesco", "At the Triennale"],
               ["The musical staff has five lines and four spaces", "True", "False"],
               ["The violin was invented in fifteenth century", "False", "True"],
               ["Antonio Vivaldi was a priest", "True", "False"]]

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

        questions_list = []
        for q in GameTest.game_elements:
            questions_list.append(q[0])
        question_number = questions_list.index(question)
        if answer == GameTest.game_elements[question_number][1]:
            return True
        else:
            return False

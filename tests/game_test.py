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
        self.__answer = False
        self.__random = random.Random()
        self.__shuffled = False

    def start(self):

        for c in self.__chosen:
            print("Question number", self.__chosen.index(c)+1)
            rand = self.__random.randint(1, 2)
            if rand == 2:
                self.__shuffled = True
                temp = c[1]
                c[1] = c[2]
                c[2] = temp

            print(c[0])
            print(c[1])
            print(c[2])
            if self.__answer and not self.__shuffled:
                print("Right!")
            elif self.__answer and self.__shuffled:
                print("Wrong!")
            elif not self.__answer and self.__shuffled:
                print("Right!")
            else:
                print("Wrong!")

            self.__shuffled = False
            print("Phase", self.__chosen.index(c)+1, "ended\n")

        print("Game ended")


g = GameTest()
g.start()

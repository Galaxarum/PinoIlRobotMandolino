import re
from threading import Thread
from time import sleep

from gpiozero import Robot


class RobotTest:
    
    SPEED = 0.2
    
    def __init__(self):
        self.__name = 'robot'
        self.__robot = Robot(left=(13, 19), right=(5, 6))
        print(f'{self.__name}: testing initiated')
        
    def __check_input(self):
        regex = re.compile('y(es)?', re.IGNORECASE)
        user_input = input(f'{self.__name}: Enter "(y)es" if the robot is moving as described')
        if (regex.match(user_input)) is not None:
            self.__robot.stop()
            return True
        else:
            self.__robot.stop()
            raise ValueError(f'{self.__name}: User abort')
        
    def forward(self):
        print(f'{self.__name}: moving forward')
        self.__robot.forward(RobotTest.SPEED)
        self.__check_input()
        
    def backward(self):
        print(f'{self.__name}: moving backward')
        self.__robot.backward(RobotTest.SPEED)
        self.__check_input()
        
    def forward_left(self):
        print(f'{self.__name}: turning left forward')
        self.__robot.forward(RobotTest.SPEED, curve_left=1)
        self.__check_input()
        
    def forward_right(self):
        print(f'{self.__name}: turning right forward')
        self.__robot.forward(RobotTest.SPEED, curve_right=1)
        self.__check_input()
        
    def backwards_left(self):
        print(f'{self.__name}: turning left backwards')
        self.__robot.backward(RobotTest.SPEED, curve_left=1)
        self.__check_input()
        
    def backwards_right(self):
        print(f'{self.__name}: turning right backwards')
        self.__robot.backward(RobotTest.SPEED, curve_right=1)
        self.__check_input()
        
    def alternate_stop(self):
        print(f'{self.__name}: Alternating 1s forward, 1s stop')

        input_thread = Thread(target=self.__check_input)
        input_thread.start()

        while input_thread.isAlive():
            self.__robot.forward(RobotTest.SPEED)
            sleep(1)
            self.__robot.stop()
            sleep(1)

    def test_all(self):
        self.forward()
        self.backward()
        self.alternate_stop()
        self.forward_left()
        self.forward_right()
        self.backwards_left()
        self.forward_right()


robot = RobotTest()

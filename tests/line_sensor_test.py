from gpiozero import LineSensor
from time import sleep
from threading import Thread


class LineSensorTest:
    def __init__(self):
        self.__name = 'line_sensor'
        self.__sensor = LineSensor(4, queue_len=10)
        self.__sensor.when_line = self.alternate_lines # lambda: print(f'{self.__name}: line found (callback)')
        self.__sensor.when_no_line = lambda: print(f'{self.__name}: line removed (callback)')
        self.__printer_thread = None
        print(f'{self.__name}: testing initiated, callbacks active')

    def print_state(self, repeat_every=0):
        print(f'{self.__name}: has value {self.__sensor.value}')
        if repeat_every > 0:
            def loop_print():
                while self.__printer_thread is not None:
                    sleep(repeat_every)
                    print(f'{self.__name}: has value {self.__sensor.value}')
            if self.__printer_thread is not None:
                old = self.__printer_thread
                self.__printer_thread = None
                old.join()
            self.__printer_thread = Thread(target=loop_print)
            self.__printer_thread.start()

    def check_line(self):
        self.__sensor.when_line = None
        print(f'{self.__name}: put line above')
        self.__sensor.wait_for_line()
        print(f'{self.__name}: line found')
        self.__sensor.when_line = lambda: print(f'{self.__name}: line found (callback)')

    def check_no_line(self):
        print(f'{self.__name}: remove line from above')
        self.__sensor.wait_for_no_line()
        print(f'{self.__name}: line removed')

    def alternate_lines(self):
        self.__sensor.when_line = None
        sleep(5)
        return


# Instantiates the line sensor and starts logging status changes
line_sensor = LineSensorTest()

from gpiozero import LineSensor
from time import sleep
from threading import Thread


class LineSensorTest:
    def __init__(self):
        self.__name = 'line sensor'
        self.__sensor = LineSensor(4, sample_rate=20)
        self.__sensor.when_line = lambda: print(f'{self.__name}: line found (callback)')
        self.__sensor.when_no_line = lambda: print(f'{self.__name}: line removed (callback)')
        self.__printer_thread = None

    def print_state(self, repeat_every=0):
        print(f'{self.__name} has value {self.__sensor.value}')
        if repeat_every > 0:
            def loop_print():
                while self.__printer_thread is not None:
                    sleep(repeat_every)
                    print(f'{self.__name} has value {self.__sensor.value}')
            if self.__printer_thread is not None:
                old = self.__printer_thread
                self.__printer_thread = None
                old.join()
            self.__printer_thread = Thread(target=loop_print)
            self.__printer_thread.start()

    def check_line(self):
        print(f'Put line under {self.__name}')
        self.__sensor.wait_for_line()
        print(f'{self.__name}: line found')

    def check_deactivation(self):
        print(f'Remove line from under {self.__name}')
        self.__sensor.wait_for_no_line()
        print(f'{self.__name}: line removed')

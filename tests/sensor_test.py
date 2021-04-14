from threading import Thread
from time import sleep


class SensorTest:
    def __init__(self, name, sensor):
        self.__name = name
        self.__sensor = sensor
        self.__sensor.when_activated = lambda: print(f'{name} activated (callback)')
        self.__sensor.when_deactivated = lambda: print(f'{name} deactivated (callback)')
        self.__printer_thread = None

    def print_state(self, repeat_every=0):
        print(f'{self.__name} is {"active" if self.__sensor.is_active else "inactive"}')
        if repeat_every > 0:
            def loop_print():
                while self.__printer_thread is not None:
                    sleep(repeat_every)
                    print(f'{self.__name} is {"active" if self.__sensor.is_active else "inactive"}')
            old = self.__printer_thread
            self.__printer_thread = None
            old.join()
            self.__printer_thread = Thread(target=loop_print)
            self.__printer_thread.start()

    def check_activation(self):
        if self.__sensor.is_active:
            print(f'{self.__name} already activated')
            return
        print(f'Activate {self.__name}')
        self.__sensor.wait_for_active()
        print(f'{self.__name} correctly activated')

    def check_deactivation(self):
        if not self.__sensor.is_active:
            print(f'{self.__name} not activated')
            return
        print(f'Deactivate {self.__name}')
        self.__sensor.wait_for_inactive()
        print(f'{self.__name} correctly deactivated')

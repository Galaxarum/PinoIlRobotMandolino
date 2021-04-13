from gpiozero import DigitalInputDevice


class LineSensorTest:
    ACTIVE_COLOR = 'black'
    INACTIVE_COLOR = 'white'

    def __init__(self):
        super().__init__()
        self.__line_sensor = DigitalInputDevice(4)
        
    def check_active(self):
        if not self.__line_sensor.is_active:
            raise ValueError(f'Ensure the sensor is activated (sees {LineSensorTest.ACTIVE_COLOR})')
        else:
            print(f'Sensor is active (seeing {LineSensorTest.ACTIVE_COLOR})')

    def check_inactive(self):
        if self.__line_sensor.is_active:
            raise ValueError(f'Ensure the sensor is deactivated (sees {LineSensorTest.INACTIVE_COLOR})')
        else:
            print(f'Sensor is inactive (seeing {LineSensorTest.INACTIVE_COLOR})')
        
    def test_wait_active(self):
        print(f'activate the sensor (show me {LineSensorTest.ACTIVE_COLOR})')
        self.__line_sensor.wait_for_active()
        print('Wait for active completed')

    def test_wait_inactive(self):
        print(f'deactivate the sensor (show me {LineSensorTest.INACTIVE_COLOR})')
        self.__line_sensor.wait_for_inactive()
        print('Wait for inactive completed')

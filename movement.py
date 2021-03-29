from gpiozero import DistanceSensor, Robot, DigitalInputDevice
from time import sleep

#sensorFront = DistanceSensor(echo='BOARD10', trigger='BOARD12', threshold_distance=0.1)
#sensorBack = DistanceSensor(echo=18, trigger=17, threshold_distance=0.1)
#robot = Robot(left=(4, 14), right=(17, 18)) #A tuple of two (or three) GPIO pins representing the forward and backward inputs of the left and right motor’s controller
line_sensor = DigitalInputDevice('BOARD12')

while True:

    #distanceFront = sensorFront.distance * 100
    #distanceBack = sensorBack.distance * 100
    #print("Distance front : %.1f" % distanceFront)
    #print("Distance back : %.1f" % distanceBack)
    print('Line sensor: ', line_sensor.is_active)
    #sleep(1)
    continue

    if distanceFront <= 10:
        robot.stop()
        robot.backward(speed=0.5)
        distanceFront.when_out_of_range = robot.stop()

    if distanceBack <= 10:
        robot.stop()
        robot.forward(speed=0.5)
        distanceBack.when_out_of_range = robot.stop()

    if line_sensor.is_active:
        robot.forward(speed=0.5)

    else:
        robot.stop()
        robot.backward(speed=0.5, curve_left=1)
        line_sensor.wait_for_inactive()
        robot.stop()
        robot.forward(speed=0.5)


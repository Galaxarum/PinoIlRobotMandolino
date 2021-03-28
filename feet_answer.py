from gpiozero import DistanceSensor
from time import sleep
import pyttsx3

engine = pyttsx3.init()
sensorLeft = DistanceSensor(echo=21, trigger=20, threshold_distance=0.1)
sensorRight = DistanceSensor(echo=18, trigger=17, threshold_distance=0.1)
end = False

while not end:

    distanceLeft = sensorLeft.distance * 100
    distanceRight = sensorRight.distance * 100
    print("Distance left : %.1f" % distanceLeft)
    print("Distance right : %.1f" % distanceRight)
    sleep(1)

    if distanceLeft <= 10:
        engine.say('Correct answer')
        engine.runAndWait()
        end = True

    if distanceRight <= 10:
        engine.say('Wrong answer')
        engine.runAndWait()
        end = True

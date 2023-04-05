import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
dac = [10,9,11,5,6,13,19,26]
number = [0,0,0,0,0,0,0,0]

GPIO.setup(dac, GPIO.OUT)

for i in range(8):
    GPIO.output(dac[i], number[i])

time.sleep(15)
GPIO.output(dac,0)
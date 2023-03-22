import RPi.GPIO as gpio
import sys
from time import sleep

dac = [26, 19, 13, 6, 5, 11, 9, 10]

gpio.setmode(gpio.BCM)
gpio.setup(2, gpio.OUT)

gpio.setup(dac, gpio.OUT, initial=gpio.LOW)
pwm = gpio.PWM(2, 1000)
pwm.start(0)

try:
    while(True):
        duty_cicle = int(input())
        pwm.ChangeDutyCycle(duty_cicle)
        print("{:.2f}".format(duty_cicle * 3.3 / 100))

finally:
    gpio.output(2, 0)
    gpio.output(dac, 0)
    gpio.cleanup()
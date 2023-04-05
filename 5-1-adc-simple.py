import RPi.GPIO as gpio
import sys
from time import sleep 
gpio.setmode(gpio.BCM)
dac=[26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

gpio.setup(dac, gpio.OUT)
gpio.setup(troyka, gpio.OUT, initial = gpio.HIGH)
gpio.setup(comp, gpio.IN)

def perev (a):
    return [int(elem) for elem in bin(a)[2:].zfill(8)]

def adc():
    for i in range (256):
        daccc = perev(i)
        gpio.output(dac, daccc)
        sleep (0.001)
        compvalue = gpio.input(comp)
        if compvalue == 0:
            return i
try:
    while (True):
        i = adc()
        if i != 0:
            print (i, '{:.2f}v'.format(3.3*i/256))

finally:
    gpio.output(dac, 0)
    gpio.cleanup()

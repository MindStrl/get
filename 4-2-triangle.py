import RPi.GPIO as gpio
import sys
from time import sleep

dac = [26, 19, 13, 6, 5, 11, 9, 10]

gpio.setmode(gpio.BCM)
gpio.setup(dac, gpio.OUT)

def translate(num, cnt):
    return [int (elem) for elem in bin(num)[2:].zfill(cnt)]

try:
    while(True):
        num = input()
        if not num.isdigit():
            print("Enter the number:")
        time_sleep = int(num) / 256 / 2
        for i in range(256):
            gpio.output(dac, translate(i, 8))
            sleep(time_sleep)
        for i in range(255, -1, -1):
            gpio.output(dac, translate(i, 8))
            sleep(time_sleep)

finally:
    gpio.output(dac, 0)
    gpio.cleanup()

import RPi.GPIO as gpio
import sys

dac = [26, 19, 13, 6, 5, 11, 9, 10]

gpio.setmode(gpio.BCM)
gpio.setup(dac, gpio.OUT)

def translate(num, cnt):
    return [int (elem) for elem in bin(num)[2:].zfill(cnt)]

try:
    while(True):
        num = input()
        if num == 'q':
            sys.exit()
        elif num.isdigit() and int(num) % 1 == 0 and 0 <= int(num) <= 255:
            gpio.output(dac, translate(int(num), 8))
            print("{:.4f}".format(int(num) / 256 * 3.3))
        elif not num.isdigit():
            print('Enter another number')

except ValueError:
    print('Enter number from 0 to 255')
finally:
    gpio.output(dac, 0)
    gpio.cleanup()
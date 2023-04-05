import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.LOW)


def adc2():
    result = 0
    i = 0
    GPIO.output(dac, [0, 0, 0, 0, 0, 0, 0, 0])
    time.sleep(1/100)
    for i in range(8):
        GPIO.output(dac[i], 1)
        time.sleep(1/100)
        if GPIO.input(comp) == 1:
            result += 2**(7-i)
        else:
            GPIO.output(dac[i], 0)
    return result



try:
    GPIO.output(troyka, 1)
    while 1:
        a = adc2()
        print("Number", a, "Voltage", a*3.3/255)
        print("\n")

finally:
    GPIO.output(dac, [0, 0, 0, 0, 0, 0, 0, 0])
    GPIO.output(troyka, 0)
    GPIO.cleanup()
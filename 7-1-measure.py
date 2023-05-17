import time
import RPi.GPIO as GPIO
import math
import numpy as np
import matplotlib.pyplot as plt

dac = [26, 19, 13, 6, 5 ,11, 9 ,10]
leds = [24, 25, 8, 7, 12, 15, 20 ,21]
comp = 4
troyka = 17

bits = len(dac)
levels = 256
maxVoltage = 3.3
counter = 0

min_percent = 24
max_percent = 94
sleep_time= 0.001

data = []
measurement = []

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(leds, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.LOW)

# This function convers decimal value to the 
# binary in order to display in usin leds
def decimal2binary(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

def num2dac(value):
    signal = decimal2binary(value)
    GPIO.output(dac, signal)
    return signal

# This function returns the current value of voltage
def adc(value):
    return (maxVoltage / levels) * value


def dec_to_bin(value):
    GPIO.output(leds, 0)
    percent =(100 * (voltage / 3.3))
    leds_val = (int)(percent / 12.5)
    last_leds = 7-leds_val
    # print("Leds  {}".format(leds_val))
    # print("last_leds {}".format(last_leds))

    if(math.isclose(voltage, 3.3, rel_tol = 0.2)):
        GPIO.output(leds, 1)
    for i in range(leds_val):
        GPIO.output(leds[i], 1)
    for g in range(7, leds_val, -1):
        GPIO.output(leds[g], 0)

# This function adds new data to the list
def add_data(index, cur_voltage):
    data.append(cur_voltage)
    measurement.append(index)

# This function converts the list to the array 
def conver_list():
    np.array(data)
    np.array(measurement)

# This function plots the graph
def plot_graph():
    conver_list()
    plt.title("ADC value depending on number of measurement")
    plt.xlabel('Measurement number')
    plt.ylabel('ADC value')
    plt.plot(measurement, data, color="red")
    plt.savefig('ADC_fig.png')

    plt.show()

try:
    bool_1 = True
    bool_2 = False

    while bool_1:
        GPIO.output(troyka, GPIO.HIGH)  
        cur_signal_val = 0
        
        for i in range(7, -1, -1):
            cur_signal_val += 2**i

            signal = decimal2binary(cur_signal_val) 
            GPIO.output(dac, signal)
            voltage = adc(cur_signal_val)

            time.sleep(sleep_time)
            comp_value = GPIO.input(comp)

            if comp_value == 0:
                cur_signal_val -= 2**i

        percent = (100 * (voltage / 3.3))
        if(percent < min_percent):
            bool_1 = False
            bool_2 = True

        print("Percents {}, ADC value {}, Volage {} V\n".format(percent, cur_signal_val, voltage))

    GPIO.output(troyka, GPIO.LOW)  
    t0 = time.time()
    while bool_2:
        cur_signal_val = 0
        
        for i in range(7, -1, -1):
            cur_signal_val += 2**i

            signal = decimal2binary(cur_signal_val) 
            GPIO.output(dac, signal)
            voltage = adc(cur_signal_val)

            time.sleep(sleep_time)
            comp_value = GPIO.input(comp)

            if comp_value == 0:
                cur_signal_val -= 2**i

        add_data(counter, cur_signal_val)
        counter += 1
        dec_to_bin(voltage)

        percent = (100 * (voltage / 3.3))
        if(percent < min_percent):
            bool_2 = False
        if(percent > max_percent):
            GPIO.output(troyka, GPIO.HIGH)  
        
        print("Percents {}, ADC value {}, Volage {} V\n".format(percent, cur_signal_val, voltage))

finally:
    t1 = time.time()
    total_time = t1 -t0
    print("Total time = {}".format(total_time))
    print("Time of one measurement = {}".format(sleep_time))
    print("Step quant  = {}".format(maxVoltage/levels))
    print("Average frequency of dicr = {}".format(1/sleep_time))
    plot_graph()

    with open('data.txt', 'w') as data_txt:
        for i in data:
            data_txt.write(f"{i}\n")
    
    with open('settings.txt', 'w') as settings_txt:
        settings_txt.write(f"Total time {total_time} s\n")
        settings_txt.write(f"Step discr {sleep_time} \n")
        settings_txt.write(f"Discr freq  {1/sleep_time} \n")
        settings_txt.write(f"Step quant  {maxVoltage/levels} \n")
        # settings_txt.write(f"Total time {total_time} s\n")

    GPIO.output(dac, GPIO.LOW)
    GPIO.output(troyka, GPIO.HIGH)
    GPIO.output(leds, GPIO.LOW)
    GPIO.cleanup()

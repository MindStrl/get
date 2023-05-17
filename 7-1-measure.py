import RPi.GPIO as GPIO
import time 
from matplotlib import pyplot 
       
def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

    
def adc():
    value = 0
    for i in range(7, -1,  -1):
        value += 2**i
        GPIO.output(dac, dec2bin(value))
        time.sleep(0.001)
        comp_value = GPIO.input(comp)
        if comp_value == 0:
            value -= 2**i
        
    return value

GPIO.setmode(GPIO.BCM) 

leds = [21, 20, 16, 12, 7, 8, 25, 24] 
GPIO.setup(leds, GPIO.OUT) 

dac = [26, 19, 13, 6, 5, 11, 9, 10] 
GPIO.setup(dac, GPIO.OUT, initial = GPIO.HIGH) 

comp = 4 
troyka = 17 
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH) 
GPIO.setup(comp, GPIO.IN) 


    
try: 
    voltage = 0 
    result_exp = [] 
    time_start = time.time() 
    point = 0 

    print('Зарядка конденсатора') 
    while voltage < 256*0.89: 
        voltage = adc() 
        print(voltage)
        result_exp.append(voltage) 
        time.sleep(0)
        point += 1 
        GPIO.output(leds, dec2bin(voltage)) 

    GPIO.setup(troyka, GPIO.OUT, initial = GPIO.LOW) 

    print('Разрядка конденсатора') 
    while voltage > 256*0.02: 
        voltage = adc() 
        print(voltage)
        result_exp.append(voltage) 
        time.sleep(0) 
        point += 1 
        GPIO.output(leds, dec2bin(voltage)) 

    time_exp = time.time()-time_start 
        
    print('Запись данных в файл') 
    with open('data.txt', 'w') as f: 
        for i in result_exp: 
            f.write(str(i) + '\n') 
    with open('settings.txt', 'w') as f: 
        f.write(str(1/(time_exp/point)) + '\n') 
        f.write('0.01289') 
        
    print('Длительность эксперимента {}, Период измерения {}, Частота дискретизации {}, Шаг квантования {}'.format(time_exp, time_exp/point, 1/(time_exp/point), 0.013)) 
    
    print('Графики') 
    y=[i/256*3.3 for i in result_exp] 
    x=[i*time_exp/point for i in range(len(result_exp))] 
    pyplot.plot(x, y) 
    pyplot.show() 

finally: 
    GPIO.output(leds, 0) 
    GPIO.output(dac, 0) 
    GPIO.cleanup()
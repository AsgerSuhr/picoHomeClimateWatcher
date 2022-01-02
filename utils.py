from machine import UART
import time, _thread
from machine import Pin
import utime as time
from dht import DHT11
from uartCom import uartSend

LED_ONBOARD = Pin(25, Pin.OUT)

def picoBlink(amount, delay=0.5):
    '''Blinks the onboard LED on the pico'''
    for i in range(amount):
        LED_ONBOARD.value(1)
        time.sleep(delay)
        LED_ONBOARD.value(0)
        time.sleep(delay)

def writeLog(data, write_type, filename = 'log'):
    '''Writes a log file'''
    write_types = ['w','a']
    if write_type not in write_types:
        raise ValueError(f'Write type is not supported, has to be one of these {str(write_types)}')
    
    with open(f'{filename}.txt', write_type) as f:
        f.write('\n' + str(data))    


from machine import UART
import time
from machine import Pin
import utime as time
from uartCom import uartSend
from utils import *

class Esp01():
    def __init__(self, SSID, PSSW):
        self.uart = UART(1,115200)
        writeLog('', 'w', filename='setup')
        self.SSID = SSID 
        self.PSSW = PSSW
        self.LED_pico = Pin(25, Pin.OUT)

    def blink(self, amount=1, delay=0.5):
        '''blinks the LED on the pico'''
        for i in range(amount):
            self.LED_pico.value(1)
            time.sleep(delay)
            self.LED_pico.value(0)
            time.sleep(delay)
            
    def setMode(self, mode):
        '''Sets the esp device WiFi connection mode'''
        if mode == 'NULL':
            mode = '0'
        elif mode == 'Station':
            mode = '1'
        elif mode == 'SoftAP':
            mode = '2'
        elif mode == 'SoftAP+Station':
            mode = '3'

        res = uartSend(f'AT+CWMODE={mode}', delay=2)
        print(res)
        writeLog(res, 'a', filename='setup')
    
    def WiFiConnect(self):
        '''connects to the wifi'''
        res = uartSend(f'AT+CWJAP="{self.SSID}","{self.PSSW}"', delay = 10)
        print(res)
        writeLog(res, 'a', filename='setup')
    
    def enableMultipleConnections(self, enable=True):
        '''enable multiple connections to the pico'''
        if enable:
            #enable multi connection mode
            res = uartSend('AT+CIPMUX=1', delay=1)
            self.blink(amount=2)
        else:
            #disable multi connection mode
            res = uartSend('AT+CIPMUX=0', delay=1)
            self.blink(amount=1)

        print(res)
        writeLog(res, 'a', file='setup')

    def postHTTP(self, message, ip_adress, port):
    
        # clearing the log file
        writeLog('', 'w', filename='HttpPostLog')
        
        # Establishing TCP connection
        res = uartSend(f'AT+CIPSTART=0,"TCP",{ip_adress},{port}', delay=4)
        print(res)
        writeLog(res, 'a', filename='HttpPostLog')

        # Create HTTP POST request and send it to the server
        val = f'POST / HTTP/1.1\r\nHost: 192.168.0.38\r\nUser-Agent: Mozilla\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(message)}\r\n\r\n{message}'

        # Tell the esp8266 we want to send data through the TCP connection. 0 is the ID of the connection that we established earlier
        res = uartSend('AT+CIPSEND=0,' + str(len(val)), delay=5)
        print(res)
        writeLog(res, 'a', filename='HttpPostLog')

        # Now we give the esp8266 the data
        res = uartSend(val, delay=10)
        print(res)
        writeLog(res)
        self.blink(10, delay=0.1)

        # We try and close the connection
        res = uartSend('AT+CIPCLOSE=0', delay=4)
        print(res)
        writeLog(res, 'a', filename='HttpPostLog')
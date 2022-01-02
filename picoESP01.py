from machine import UART
import time, _thread
from machine import Pin
import utime as time
from dht import DHT11
from uartCom import uartSend
from utils import *

class ATcom():
    def __init__(self, SSID, PSSW):
        self.uart = UART(1,115200)
        writeLog('', 'w', filename='setup')
        self.SSID = SSID 
        self.PSSW = PSSW

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
        res = uartSend(f'AT+CWJAP="{self.SSID}","{self.PSSW}"', delay = 10)
        print(res)
        writeLog(res, 'a', filename='setup')
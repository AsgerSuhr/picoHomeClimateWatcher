#Using ESP8266 wifi module
from machine import UART
import machine
import _thread
import time
from machine import Pin, I2C
import utime as time
from dht import DHT11, InvalidChecksum


def uartSerialRxMonitor(command):
    recv=bytes()
    while uart.any()>0:
        recv+=uart.read(1)
    res=recv.decode('utf-8')
    #erase_len=len(command)+5
    #res = res[erase_len:]
    return res

def uartSend(command, delay=1):
    send=command
    uart.write(send+'\r\n')
    time.sleep(delay)
    res=uartSerialRxMonitor(send)
    return res

uart = UART(1,115200)
print('-- UART Serial --')
print('>', end='')

#factory reset
#res = uartSend('AT+RESTORE', delay=2)
#print(res)

#reset esp8266
res = uartSend('AT+RST', delay=4)
print(res)

#connect to router
#res = uartSend('AT+CWJAP="WiFimodem-7D90","zwy3uznxkd"', delay = 10)
#print(res)

while True:
    user_input = input('Command: ')
    user_d = int(input('delay: '))
    res = uartSend(user_input, delay=user_d)
    print(res)
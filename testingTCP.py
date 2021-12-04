#Code for Simple Rasberry Pi PICO Web server
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

pin = Pin(14, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(pin)

uart = UART(1,115200)
print('-- UART Serial --')
print('>', end='')
#res = uartSend('AT+RST', delay=5)
#print(res)
#Close TCP connection if any
res = uartSend('AT+CIPSTATUS', delay=1)
if int(''.join(x for x in res if x.isdigit())) == 3:
    res = uartSend('AT+CIPCLOSE=0', delay=1)
    print(res)

#enable multi connection mode
res = uartSend('AT+CIPMUX=1', delay=1)
print(res)

#configure as SoftAP+station mode
res = uartSend('AT+CWMODE=3', delay=2)
print(res)

#listen for wifi networks in the area
#res = uartSend('AT+CWLAP', delay=10)
#print(res)

#connect to router
#res = uartSend('AT+CWJAP="WiFimodem-7D90","zwy3uznxkd"', delay = 10)
#print(res)

#connect to router
res = uartSend('AT+PING="192.168.0.5"', delay = 1)
print(res)

# Establishing TCP connection
#res = uartSend('AT+CIPSTART=0,"TCP","192.168.0.5",5000', delay=4)
#print(res)

#res = uartSend('AT+CIPSTATUS', delay=10)
#print(res)

#Here the code runs indefinitely 
while True:
    res = uartSend('AT+CIPSTART=0,"TCP","192.168.0.5",5000', delay=4)
    print(res)
    
    #temperature reading
    reading_temp  = (sensor.temperature)
    reading_humidity = (sensor.humidity)
    package = f'PICO=Temperature: {str(reading_temp)} Humidity: {str(reading_humidity)}'
    
    val = 'GET / HTTP/1.1\r\nHost: 192.168.0.38\r\nUser-Agent: Mozilla\r\nContent-Type: application/x-www-form-urlencoded\r'
    val = f'POST / HTTP/1.1\r\nHost: 192.168.0.38\r\nUser-Agent: Mozilla\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(package)}\r\n\r\n{package}'
    
    res = uartSend('AT+CIPSEND=0,' + str(len(val)), delay=5)
    print(res)
    res = uartSend(val, delay=10)
    print(res)
    res = uartSend('AT+CIPCLOSE=0', delay=4)
    print(res)
    time.sleep(10)

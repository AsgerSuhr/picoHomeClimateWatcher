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

#factory reset
#res = uartSend('AT+RESTORE', delay=2)
#print(res)

#reset esp8266
#res = uartSend('AT+RST', delay=4)
#print(res)

#configure as SoftAP+station mode
res = uartSend('AT+CWMODE=1', delay=2)
print(res)

#Device info
#res = uartSend('AT+GMR', delay=5)
#print(res)

#listen for wifi networks in the area
#res = uartSend('AT+CWLAP', delay=10)
#print(res)

#connect to router
res = uartSend('AT+CWJAP="WiFimodem-7D90","zwy3uznxkd"', delay = 10)
print(res)

# Setup AP:
# AT+CWSAP=ssid,pwd,chl,ecn
# ssid/pwd=name and password of the WIFI AP
# chl=number of connection channels
# ecn=encryption mode (1=OPEN, 2=WPA_PSK, 3=WPA2_PSK, 4=WPA_WPA2_PSK)
#res = uartSend('AT+CWSAP="esp8266","",11,0,3', delay=10)
#print(res)

#enable multi connection mode
res = uartSend('AT+CIPMUX=1', delay=1)
print(res)

# Enable the TCP server with port 80,
res = uartSend('AT+CIPSERVER=1,80', delay=10)
print(res)

#IP adress
res = uartSend('AT+CIFSR', delay=4)
print(res)

res = uartSend('AT+CIPSTATUS', delay=10)
print(res)

#temperature reading
#sensor_temp = machine.ADC(4)
#conversion_factor = 3.3 / (65535)

#Here the code runs indefinitely 
while True:
    #temperature reading
    #reading_temp = sensor_temp.read_u16() * conversion_factor 
    #temperature = 27 - (reading_temp - 0.706)/0.001721
    reading_temp  = (sensor.temperature)
    reading_humidity = (sensor.humidity)
    #Place basic code for HTML page display
    val='<head><title>Rasberry Pi Pico Server</title></head><body><p>Temperature is: '+str(int(reading_temp))+' deg & Humidity is: '+ str(int(reading_humidity)) +' '+'</p></body>'
    length=str(len(val))
    print(val, length)
    
    res = uartSend('AT+CIPSEND=0,'+length, delay=5)
    print("Data sent-> "+res)
    
    res = uartSend(val, delay=10)
    print(res)
    #time.sleep(10)
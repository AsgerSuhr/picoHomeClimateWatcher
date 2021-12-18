'''
Code for Simple Rasberry Pi PICO Web server, using ESP8266 wifi module.
Link to the AT commands docs: https://docs.espressif.com/projects/esp-at/en/latest/AT_Command_Set/Basic_AT_Commands.html
deep sleep blog for pico in micropython: https://ghubcoder.github.io/posts/deep-sleeping-the-pico-micropython/
micropython deepsleep repo: https://github.com/ghubcoder/micropython-pico-deepsleep
deep sleep blog for pico in C: https://ghubcoder.github.io/posts/awaking-the-pico/
how to program esp01: https://nematicslab.com/how-to-program-esp01/
ESP01 deepsleep: https://www.instructables.com/Enable-DeepSleep-on-an-ESP8266-01/
'''
from machine import UART
import time
from machine import Pin
import utime as time
from dht import DHT11
from uartCom import uartSend
import picosleep

SLEEP = 60

# activate pins for the DHT sensor
pin = Pin(14, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(pin)

# activate the UART pins serial on port 115200
uart = UART(1,115200)
print('-- UART Serial --')
print('>', end='')

res = uartSend('AT+CWQAP', delay=2)
print(res)

res = uartSend('AT+RESTORE', delay=2)
print(res)
#If there's a TCP connection, reset the device (couldn't get AT+CIPCLOSE to work?)
res = uartSend('AT+CIPSTATUS', delay=1)
res = uartSend('AT+RST', delay=5)
print(res)
if res:
    if int(''.join(x for x in res if x.isdigit())) == 3:
        res = uartSend('AT+RST', delay=5)
        print(res)
else:
    #factory reset
    res = uartSend('AT+RESTORE', delay=2)
    print(res)    
    res = uartSend('AT+RST', delay=5)
    print(res)
    
#enable multi connection mode
res = uartSend('AT+CIPMUX=1', delay=1)
print(res)

#configure as SoftAP+station mode
res = uartSend('AT+CWMODE=3', delay=2)
print(res)

#connect to router
res = uartSend('AT+CWJAP="WiFimodem-7D90","zwy3uznxkd"', delay = 10)
print(res)

#connect to router
res = uartSend('AT+PING="192.168.0.5"', delay = 1)
print(res)

#Here the code runs indefinitely 
while True:
    # Establishing TCP connection
    res = uartSend('AT+CIPSTART=0,"TCP","192.168.0.5",5000', delay=4)
    print(res)
    
    #temperature reading
    reading_temp  = (sensor.temperature)
    reading_humidity = (sensor.humidity)
    package = f'PICO=Temperature: {str(reading_temp)} Humidity: {str(reading_humidity)}'
    
    # Create HTTP POST request and send it to the server
    #val = 'GET / HTTP/1.1\r\nHost: 192.168.0.38\r\nUser-Agent: Mozilla\r\nContent-Type: application/x-www-form-urlencoded\r'
    val = f'POST / HTTP/1.1\r\nHost: 192.168.0.38\r\nUser-Agent: Mozilla\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(package)}\r\n\r\n{package}'
    
    # Tell the esp8266 we want to send data through the TCP connection. 0 is the ID of the connection that we established earlier
    res = uartSend('AT+CIPSEND=0,' + str(len(val)), delay=5)
    print(res)

    # Now we give the esp8266 the data
    res = uartSend(val, delay=10)
    print(res)
    
    # We try and close the connection
    res = uartSend('AT+CIPCLOSE=0', delay=4)
    print(res)

    # and then we sleep
    for i in range(10):
        #picosleep.seconds(SLEEP)
        time.sleep(60)


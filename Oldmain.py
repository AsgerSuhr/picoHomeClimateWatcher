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
import time, _thread
from machine import Pin
import utime as time
from dht import DHT11
from uartCom import uartSend

SLEEP_MIN = 30
SSID = 'WiFimodem-7D90'
PSSW = 'zwy3uznxkd'

# activate pins for the DHT sensor and the button
pin = Pin(14, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(pin)
button_pin = Pin(16, Pin.IN, Pin.PULL_DOWN)
led_onboard = Pin(25, Pin.OUT)

def blink(amount, delay=0.5):
    for i in range(amount):
        led_onboard.value(1)
        time.sleep(delay)
        led_onboard.value(0)
        time.sleep(delay)

def writeTo(data, file = 'log', append=True):
    if append:
        tpe = 'a'
    else:
        tpe = 'w'
    with open(f'{file}.txt', tpe) as f:
        f.write('\n' + str(data))    
    
# activate the UART pins serial on port 115200
uart = UART(1,115200)
print('-- UART Serial --')
print('>', end='')
blink(2)
writeTo('', file='setup', append=False)

#configure as station mode
try:
    res = uartSend('AT+CWMODE=1', delay=2)
    print(res)
    writeTo(res, file='setup')
    blink(2)
except Exception as err:
    with open('error.txt', 'w') as f:
        f.write(str(err))
#If there's a TCP connection, reset the device (couldn't get AT+CIPCLOSE to work?)
res = uartSend('AT+CIPSTATUS', delay=1)
print(res)
writeTo(res, file='setup')
if res:
    blink(25, delay=0.05)
    resp_int = int(''.join(x for x in res if x.isdigit()))
    if resp_int == 3:
        res = uartSend('AT+CIPCLOSE', delay=5)
        print(res)

    elif resp_int != 3 and resp_int != 4:
        #connect to router if the ESP isn't connected
        res = uartSend(f'AT+CWJAP="{SSID}","{PSSW}"', delay = 10)
        print(res)
else:
    #factory reset
    #res = uartSend('AT+RESTORE', delay=2)
    #print(res)    
    res = uartSend('AT+RST', delay=5)
    print(res)
    
#enable multi connection mode
res = uartSend('AT+CIPMUX=1', delay=1)
print(res)
writeTo(res, file='setup')
blink(2)

#pings flask server
res = uartSend('AT+PING="192.168.0.5"', delay = 1)
print(res)
writeTo(res, file='setup')
#Here the code runs indefinitely 
while True:
    # Establishing TCP connection
    res = uartSend('AT+CIPSTART=0,"TCP","192.168.0.5",5000', delay=4)
    print(res)
    writeTo(res, append=False)
    
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
    writeTo(res)
    # Now we give the esp8266 the data
    res = uartSend(val, delay=10)
    print(res)
    writeTo(res)
    blink(10, delay=0.1)
    # We try and close the connection
    res = uartSend('AT+CIPCLOSE=0', delay=4)
    print(res)
    writeTo(res)
    # and then we sleep
    time.sleep(SLEEP_MIN * 60)


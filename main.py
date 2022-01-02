from oldMain import SLEEP_MIN
from picoESP01 import Esp01
from machine import Pin
from dht import DHT11
import utime

# Specifying sleep time in minutes
SLEEP_MIN = 30

# Setting up WiFI module and sensor
esp01 = Esp01('WiFimodem-7D90', 'zwy3uznxkd')
pin = Pin(14, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(pin)

esp01.setMode('Station')
esp01.WiFiConnect()
esp01.enableMultipleConnections(enable=True)

while True:
    #temperature reading
    reading_temp  = (sensor.temperature)
    reading_humidity = (sensor.humidity)
    package = f'PICO=Temperature: {str(reading_temp)} Humidity: {str(reading_humidity)}'    

    # send HTTP post with the temperature readings
    esp01.postHTTP(package, '192.168.0.5', '5000')

    # pico sleeps
    utime.sleep(SLEEP_MIN * 60)

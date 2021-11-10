from machine import Pin, I2C
import utime as time
from dht import DHT11, InvalidChecksum

pin = Pin(14, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(pin)

while True:
    time.sleep(5)
    
    t  = (sensor.temperature)
    h = (sensor.humidity)
    print("Temperature: {}".format(sensor.temperature))
    print("Humidity: {}".format(sensor.humidity))

    time.sleep(5)
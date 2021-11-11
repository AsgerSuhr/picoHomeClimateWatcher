from machine import UART
import machine
import _thread
import time



uart = UART(1,115200)

print('-- UART Serial --')
print('>', end='')


#Define all constants
SSID = "YOUR WIFI SSID"
PASSWORD = "YOUR WIFI PASSWORD"
TOKEN = "YOUR UBIDOTS TOKEN"
DEVICE_LABEL="raspberry-pi-pico"
VARIABLE_LABEL="temperature"
USER_AGENT="randomstring"


def uartSerialRxMonitor(command):
    recv=bytes()
    while uart.any()>0:
        recv+=uart.read(1)
    res=recv.decode('utf-8')
    erase_len=len(command)+5
    res = res[erase_len:]
    return res

def wifi_is_connected():
    res=""
    send = "AT+CWJAP?"
    uart.write(send+'\r\n')
    time.sleep(4)
    res=wifi_is_connected_response(send)
    if res=="No AP":
        print("WiFi Status:"+res)
    return res

def wifi_is_connected_response(command):
    recv=bytes()
    while uart.any()>0:
        recv+=uart.read(1)
    res=recv.decode('utf-8')
    erase_len=len(command)+3
    res = res[erase_len:]
    res = res[:5]
    return res

def wifi_connect(SSID,PASSWORD):
    res=""
    send = "AT+CWJAP=\""+SSID+"\",\""+PASSWORD+"\""
    uart.write(send+'\r\n')
    time.sleep(7)
    res=uartSerialRxMonitor(send)
    print("Attempting to connect to WiFi..."+res)
    return res

def sendhttp(value):
    
    send='AT+CIPSTART="TCP","industrial.api.ubidots.com",80'
    uart.write(send+'\r\n')
    time.sleep(2)
    
    #build payload and find its length
    payload= '{"'+VARIABLE_LABEL+'":'+str(value)+'}'
    payload_length= len(payload)
    
    #find request length
    req_length = 147
    req_length+= len(DEVICE_LABEL+TOKEN+str(payload_length)+payload+USER_AGENT)
    
    send="AT+CIPSEND="+str(req_length)
    uart.write(send+'\r\n')
    time.sleep(0.6)
    
    send="POST /api/v1.6/devices/"+DEVICE_LABEL+" HTTP/1.1"
    uart.write(send+'\r\n')
    time.sleep(0.6)
    
    send="Host:industrial.api.ubidots.com"
    uart.write(send+'\r\n')
    time.sleep(0.6)
    
    send="User-Agent:"+USER_AGENT
    uart.write(send+'\r\n')
    time.sleep(0.6)
    
    send="X-Auth-Token:"+TOKEN
    uart.write(send+'\r\n')
    time.sleep(0.6)
    
    send="Content-Type:application/json"
    uart.write(send+'\r\n')
    time.sleep(0.6)
    
    send="Content-Length:"+str(payload_length)
    uart.write(send+'\r\n')
    time.sleep(0.6)
    
    send=""
    uart.write(send+'\r\n')
    time.sleep(0.6)
        
    uart.write(payload+'\r\n')
    
    send=""
    uart.write(send+'\r\n')
    time.sleep(0.6)
    
    print("Data sent: "+payload)
    
    
#Here the code begins to run (Similar to arduino's setup())

wifi_connect(SSID,PASSWORD)
time.sleep(10)

send='AT+CWMODE=1'
uart.write(send+'\r\n')
time.sleep(1)
    
send='AT+CIPMUX=0'
uart.write(send+'\r\n')
time.sleep(1)

#temperature reading
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

print("Setup done")



#Here the code runs indefinitely (Similar to arduino's loop())


while True:
    #temperature reading
    reading_temp = sensor_temp.read_u16() * conversion_factor 
    temperature = 27 - (reading_temp - 0.706)/0.001721
    
    state = wifi_is_connected()
    
    if state=="No AP":
        time.sleep(10)
        wifi_connect(SSID,PASSWORD)
       
   
    sendhttp(temperature)
    time.sleep(3)
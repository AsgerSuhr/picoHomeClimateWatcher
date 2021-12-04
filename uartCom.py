from machine import UART
from time import sleep

uart = UART(1,115200)

def uartSerialRxMonitor(command:str) -> str:
    '''Monitors the response over UART'''
    recv=bytes()
    while uart.any()>0:
        recv+=uart.read(1)
    res=recv.decode('utf-8')
    #erase_len=len(command)+5
    #res = res[erase_len:]
    return res

def uartSend(command:str, delay:int=1) -> str:
    '''Communicates via UART, and returns the response'''
    send=command
    uart.write(send+'\r\n')
    sleep(delay)
    res=uartSerialRxMonitor(send)
    return res
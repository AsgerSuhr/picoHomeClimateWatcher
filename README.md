# picoHomeClimateWatcher
logs the humidity and temperature and lets you know when its time to air out.

# flashing AT commands firmware esp8266/esp01
If you wanna take advantage of the AT firmware you gotta flash the esp with a usb to serial (FTDI) converter. You can flash it with the esptool.py:

esptool.py -p [port] write_flash 0x000000 [path]
esptool.py -p /dev/ttyUSB0 write_flash 0x000000 ai-thinker-v1.1.1.bin

remember GPIO0 has to be connected to ground, when doing this. So connect GPIO0 to ground and then reset the esp01 and run the command above. 
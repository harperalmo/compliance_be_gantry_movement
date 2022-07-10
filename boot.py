'''
This boot.py file is boilerplate for creating a network connection
'''
#This is the official way to import the socket library
try:
    import usocket as socket
except:
    import socket

from machine import Pin
#Functionality to connect to a WiFi net
import network

#Turns offvendor OS debug messages
import esp
esp.osdebug(None)

#run a garbage collector
import gc
gc.collect()

ssid = 'BenchcreekGuest_24'
password = 'b1gc0vefun'

station = network.WLAN(network.STA_IF) #create station interface
station.active(True)                   #active it
station.connect(ssid, password)        #connect to router

#do not proceed until we have a wlan connection
while not station.isconnected():
    pass

#tell us we are connected and display net parms
print('WLAN connection successful')
print(station.ifconfig())
led = Pin(12, Pin.OUT)
print('\n --== boot.py code complete ==--\n')


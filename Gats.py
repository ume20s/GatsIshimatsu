import time
import numpy as np
import wiringpi as pi
import subprocess
from subprocess import Popen
import socket
import sys

SPI_CH = 0
READ_CH = 0
direction = 0
pi.wiringPiSPISetup(SPI_CH, 1000000 )

motor11_pin = 23
motor12_pin = 24
motor21_pin = 22
motor22_pin = 27
pi.wiringPiSetupGpio()
pi.pinMode( motor11_pin, 1 )
pi.pinMode( motor12_pin, 1 )
pi.pinMode( motor21_pin, 1 )
pi.pinMode( motor22_pin, 1 )
pi.softPwmCreate( motor11_pin, 0, 100)
pi.softPwmCreate( motor12_pin, 0, 100)
pi.softPwmCreate( motor21_pin, 0, 100)
pi.softPwmCreate( motor22_pin, 0, 100)
pi.softPwmWrite( motor11_pin, 0 )
pi.softPwmWrite( motor12_pin, 0 )
pi.softPwmWrite( motor21_pin, 0 )
pi.softPwmWrite( motor22_pin, 0 )

while True:
    try:
        pi.softPwmWrite( motor11_pin, 0 )
        pi.softPwmWrite( motor12_pin, 80 )
        pi.softPwmWrite( motor21_pin, 0 )
        pi.softPwmWrite( motor22_pin, 80 )
        
        buffer = 0x6800 |  (0x1800 * READ_CH ) 
        buffer = buffer.to_bytes( 2, byteorder='big' )
        
        pi.wiringPiSPIDataRW( SPI_CH, buffer )
        value = ( buffer[0] * 256 + buffer[1] ) & 0x3ff
        print ("value :" , value)
        if value > 1022:
            time.sleep(0.15)
            cmd = "aplay ite.wav"
            proc = Popen( cmd .strip().split(" ") )
            pi.softPwmWrite( motor11_pin, 0 )
            pi.softPwmWrite( motor12_pin, 0 )
            pi.softPwmWrite( motor21_pin, 0 )
            pi.softPwmWrite( motor22_pin, 0 )
            time.sleep(1)
            cmd = "aplay gats.wav"
            proc = Popen( cmd .strip().split(" ") )
            pi.softPwmWrite( motor11_pin, 25 )
            pi.softPwmWrite( motor12_pin, 0 )
            pi.softPwmWrite( motor21_pin, 25 )
            pi.softPwmWrite( motor22_pin, 0 )
            time.sleep(1.5)
            cmd = "aplay gats.wav"
            proc = Popen( cmd .strip().split(" ") )
            pi.softPwmWrite( motor11_pin, 25 )
            pi.softPwmWrite( motor12_pin, 0 )
            pi.softPwmWrite( motor21_pin, 25 )
            pi.softPwmWrite( motor22_pin, 0 )
            time.sleep(1.2)
            pi.softPwmWrite( motor11_pin, 0 )
            pi.softPwmWrite( motor12_pin, 0 )
            pi.softPwmWrite( motor21_pin, 0 )
            pi.softPwmWrite( motor22_pin, 0 )
            time.sleep(1.0)
            if direction == 0:
                pi.softPwmWrite( motor11_pin, 0 )
                pi.softPwmWrite( motor12_pin, 30 )
                pi.softPwmWrite( motor21_pin, 30 )
                pi.softPwmWrite( motor22_pin, 0 )
                direction = 1
            else:
                pi.softPwmWrite( motor11_pin, 30 )
                pi.softPwmWrite( motor12_pin, 0 )
                pi.softPwmWrite( motor21_pin, 0 )
                pi.softPwmWrite( motor22_pin, 30 )
                direction = 0
            time.sleep(2.3)
            pi.softPwmWrite( motor11_pin, 0 )
            pi.softPwmWrite( motor12_pin, 0 )
            pi.softPwmWrite( motor21_pin, 0 )
            pi.softPwmWrite( motor22_pin, 0 )
            time.sleep(1.0)

    except KeyboardInterrupt:
        break

pi.softPwmWrite( motor11_pin, 0 )
pi.softPwmWrite( motor12_pin, 0 )
pi.softPwmWrite( motor21_pin, 0 )
pi.softPwmWrite( motor22_pin, 0 )

print('Stop Streaming')

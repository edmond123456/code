#!/usr/bin/env python
import serial
from naoqi import ALProxy
import time
import math
import numpy as np
import almath
import sys
import pyautogui
import csv
import datetime
import random

def DataToStr(x,y):
	if isinstance(x, str):
		return x + chr(y)
	else:
		return chr(x) + chr(y)

con = serial.Serial("COM3",
					115200,
					parity = serial.PARITY_EVEN,
					stopbits = serial.STOPBITS_ONE,
					timeout = 1,)
print con.portstr

def cal0(a):
    if 184<=a<710:
        b=int(-2.8885e-8*(a-184)**3+1.1284e-4*(a-184)**2+0.4239*(a-184)+6500)
    elif 710<=a<1170:
        b=int(-2.8885e-8*(a-710)**3+6.7255e-5*(a-710)**2+0.5187*(a-710)+6750)
    elif 1170<=a<1598:
        b=int(5.5660e-8*(a-1170)**3+2.7394e-5*(a-1170)**2+0.5622*(a-1170)+7000)
    elif 1598<=a<1996:
		b=int(-1.7320e-7*(a-1598)**3+9.8861e-5*(a-1598)**2+0.6162*(a-1598)+7250)
    elif 1996<=a<2422:
		b=int(1.1140e-7*(a-1996)**3-1.0793e-4*(a-1996)**2+0.6126*(a-1996)+7500)
    elif 2422<=a<2852:
        b=int(-7.9618e-8*(a-2422)**3+3.4438e-5*(a-2422)**2+0.5813*(a-2422)+7750)
    elif 2852<=a<3322:
        b=int(-1.2493e-8*(a-2852)**3-6.8269e-5*(a-2852)**2+0.5668*(a-2852)+8000)
    else:
        b=int(-1.2493e-8*(a-3322)**3-8.5884e-5*(a-3322)**2+0.4943*(a-3322)+8250)
    return b


def cal1(a):
    if 238<=a<720:
        b=int(-2.1456e-8*(a-238)**3+8.3822e-5*(a-238)**2+0.4833*(a-238)+6500)
    elif 720<=a<1160:
        b=int(-2.1456e-8*(a-720)**3+5.2797e-5*(a-720)**2+0.5491*(a-720)+6750)
    elif 1160<=a<1582:
        b=int(-5.7057e-9*(a-1160)**3+2.4475e-5*(a-1160)**2+0.5831*(a-1160)+7000)
    elif 1582<=a<1994:
		b=int(-6.0376e-9*(a-1582)**3+1.7252e-5*(a-1582)**2+0.6007*(a-1582)+7250)
    elif 1994<=a<2410:
		b=int(-8.6474e-8*(a-1994)**3+9.7891e-6*(a-1994)**2+0.6119*(a-1994)+7500)
    elif 2410<=a<2872:
        b=int(5.3211e-8*(a-2410)**3-9.8130e-5*(a-2410)**2+0.5751*(a-2410)+7750)
    elif 2872<=a<3374:
        b=int(-3.2768e-8*(a-2872)**3-2.4380e-5*(a-2872)**2+0.5185*(a-2872)+8000)
    else:
        b=int(-3.2768e-8*(a-3374)**3-7.3728e-5*(a-3374)**2+0.4693*(a-3374)+8250)
    return b


t = {}
t0 = time.clock()
t[0] = t0
fmin = 0.03
p=2
num=1000

addr = range(12)

i=1
try:
	while True:

			val0=cal0(2000)
			data0 = reduce(DataToStr, [(0x80 | addr[0]), val0 >> 7, val0 &0x7f])
			#val1=int(np.sin(2 * math.pi * fmin * t[i])*2000+7500)
			val1=cal1(2300)
			data1 = reduce(DataToStr, [(0x80 | addr[1]), val1 >> 7, val1 &0x7f])
			con.write(data0)
			con.write(data1)
			#rcv = [ord(i) for i in con.read(6)]
			#print rcv
			i=i+1
			if i>num:
				break
except KeyboardInterrupt:
	con.close()


print time.clock() - t0

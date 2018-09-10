"""
pepperがレーザを追いかける （one dimension）
"""

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



ip = "192.168.1.69"
port = 9559
localip = "localhost"
localport = 51384

sys.stdout.flush()
#g = raw_input('select the robot(1:pepper, 2:virtual robot): ')
g = "1\r"
if g == "1\r":
    motion = ALProxy("ALMotion", ip, port)
    posture = ALProxy("ALRobotPosture", ip, port)
    locallization = ALProxy("ALLocalization", ip, port)
    tts = ALProxy("ALTextToSpeech", ip, port)
    awareness = ALProxy("ALBasicAwareness", ip, port)
    autoMove = ALProxy("ALAutonomousMoves", ip, port)

elif g == "2\r":
    motion = ALProxy("ALMotion", localip, localport)
    posture = ALProxy("ALRobotPosture", localip, localport)
    locallization = ALProxy("ALLocalization", localip, localport)
    tts = ALProxy("ALTextToSpeech", localip, localport)
    #awareness = ALProxy("ALBasicAwareness", localip, localport)
    #autoMove = ALProxy("ALAutonomousMoves", localip, localport)
else:
    print "no input"
    exit()

#初期位置を決定
locallization.learnHome()

addr = range(12)
val0=cal0(1998)
data0 = reduce(DataToStr, [(0x80 | addr[0]), val0 >> 7, val0 &0x7f])
val1=cal1(1994)
data1 = reduce(DataToStr, [(0x80 | addr[1]), val1 >> 7, val1 &0x7f])
con.write(data0)
con.write(data1)
#基本姿勢
posture.goToPosture("StandInit", 0.5)
#移動中の腕を固定
motion.setMoveArmsEnabled(False, False)
#腕の衝突保護を設定
motion.setExternalCollisionProtectionEnabled("Arms", False)

#tts.say("ボタンを押してください")
k = raw_input('plz press the key"s": ')
if k == "s\r":
    pass
else:
    print "no input"
    exit()

MaxAccXY = 0.55
MaxVelXY = 0.55
num = 15000  # loop time
dt = 0.005
fmin = 0.03
p = 2

t = {}
v = {}
v[0] = 0



#Q2
tts.say("始まります")
t0 = time.clock()
t[0] = t0


fmin = 0.03
p=2
num=2000


i=1
l0=0
l1=0
while True:
    t[i] = time.clock() - t0
    vp0 = 1.0 / 4.0 * (np.sin(2 * math.pi * fmin * t[i]) +
                     np.sin(2 * math.pi * fmin * p * t[i]) / p +
                     np.sin(2 * math.pi * fmin * p**2 * t[i]) / p**2 +
                     np.sin(2 * math.pi * fmin * p**3 * t[i]) / p**3 +
                     np.sin(2 * math.pi * fmin * p**4 * t[i]) / p**4)
    print vp0
    l0=vp0*1800+1998
    val0=cal0(l0)
    data0 = reduce(DataToStr, [(0x80 | addr[0]), val0 >> 7, val0 &0x7f])
    val1=cal1(1994)
    data1 = reduce(DataToStr, [(0x80 | addr[1]), val1 >> 7, val1 &0x7f])
    #con.write(data0)
    #con.write(data1)
    motion.moveToward(vp0, 0.0, 0.0,
                      [["MaxAccXY", MaxAccXY], ["MaxVelXY", MaxVelXY]])
    time.sleep(dt)
    i=i+1
    if i>num:
	    break



total_time = time.clock() - t0
print "total time: ", total_time
print "average frequency:", num / total_time
motion.stopMove()
tts.say("終わりです。")




val0=cal0(1998)
data0 = reduce(DataToStr, [(0x80 | addr[0]), val0 >> 7, val0 &0x7f])
val1=cal1(1994)
data1 = reduce(DataToStr, [(0x80 | addr[1]), val1 >> 7, val1 &0x7f])
con.write(data0)
con.write(data1)


#csvに書き込む
#matrix = np.zeros((len(t), 3))
#for i in range(len(t)):
#    matrix[i, 0] = i
#    matrix[i, 1] = t[i]
#    matrix[i, 2] = v[i]


#csvファイルへ書き込み
#now = datetime.datetime.now()
#filename = "pepper_mouse_" + now.strftime("%Y%m%d%H%M") + ".csv"
#np.savetxt(filename, matrix, delimiter=',')
















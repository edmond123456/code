# -*- coding: utf-8 -*-
"""
Created on 2018/06/28

change speed of pepper randomly in 100Hz
No load speed (rpm)  6110
Torque constant (mNm/A)  36.9
Stall torque (mNm)  820
Max Continuous torque (mNm)  130
Speed Reduction ratio   109

This time,we want to give a velocity function like v=L*sin(2*pi*f*t)/f
so in pepper_mouse_3_3, we are goint to move pepper like this way

from pepper_mouse_3_2, we could know that time for the "moveToward" function is about 0.05s

frequency of pepper should not be over 0.5Hz
velocity of pepper should not be over 0.33m/s


pepepr's movetoward command:
+1 and -1 correspond to the maximum velocity in the counterclockwise and clockwise directions, respectively.
maximum angular velocity (radians/second) 0.2~2.0 default:1.0

@author: Hua
"""

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

i = 1
while 1:
    t[i] = time.clock() - t0
    q = 1.0 / 4.0 * (np.sin(2 * math.pi * fmin * t[i]) +
                     np.sin(2 * math.pi * fmin * p * t[i]) / p +
                     np.sin(2 * math.pi * fmin * p**2 * t[i]) / p**2 +
                     np.sin(2 * math.pi * fmin * p**3 * t[i]) / p**3 +
                     np.sin(2 * math.pi * fmin * p**4 * t[i]) / p**4)

    #q=np.sin(2*math.pi*fmin*t[i])/3
    #q=2.0/3.0* ( np.sin(2 * math.pi * fmin * t[i]))
    v[i] = q * MaxVelXY
    print q

    motion.moveToward(q, q / abs(q) * 0.01, 0.0,
                      [["MaxAccXY", MaxAccXY], ["MaxVelXY", MaxVelXY]])
    time.sleep(dt)
    i += 1
    if i > num:
        break
total_time = time.clock() - t0
print "total time: ", total_time
print "average frequency:", num / total_time

motion.stopMove()
tts.say("終わりです。")

#csvに書き込む
matrix = np.zeros((len(t), 3))
for i in range(len(t)):
    matrix[i, 0] = i
    matrix[i, 1] = t[i]
    matrix[i, 2] = v[i]


#csvファイルへ書き込み
now = datetime.datetime.now()
filename = "pepper_mouse_" + now.strftime("%Y%m%d%H%M") + ".csv"
np.savetxt(filename, matrix, delimiter=',')
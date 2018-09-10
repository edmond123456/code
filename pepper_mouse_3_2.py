# -*- coding: utf-8 -*-
"""
Created on 2018/06/28

change speed of pepper randomly in 100Hz
No load speed (rpm)  6110
Torque constant (mNm/A)  36.9
Stall torque (mNm)  820
Max Continuous torque (mNm)  130
Speed Reduction ratio   109

if the time spent from minium velocity to maximum velocity is less than 0.01s
then this task could be done

condidering that the acceleration is set to 0.55 m/s2
max velocity change in 0.01s should be 0.55*0.01=0.0055 m/s
which means velocity should be [-0.00275,0.00275]m/s

Q1 could Pepper move in a velocity at 0.00275m/s?
maximum planar velocity (meters/second)  settable  0.1~0.55m/s
A1 it seems OK

100Hz COMPLETED!
However,we want to give a velocity function like v=sin(t)
so in pepper_mouse_3_3, we are goint to move pepper like that way


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



#tts.say("ボタンを押してください")
k = raw_input('plz press the key"s": ')
if k == "s\r":
    pass
else:
    print "no input"
    exit()




MaxAccXY = 0.55
MaxVelXY = 0.1
num=1000 # loop time
#vx=0.0275

# Q1
#motion.moveToward(vx, 0.0, 0.0,  [["MaxAccXY", MaxAccXY],["MaxVelXY", MaxVelXY]])
#time.sleep(10.0)
#motion.stopMove()


#Q2
tts.say("始まります")
t0=time.clock()
i = 1
while 1:
    #v=vx*random.random()
    v=(random.random()-0.5)*2
    print v
    #motion.moveToward(v,0,0)
    motion.moveToward(v, 0.0, 0.0,  [["MaxAccXY", MaxAccXY],["MaxVelXY", MaxVelXY]])
    time.sleep(0.005)
    i += 1
    if i > num:
        break
dt=time.clock() - t0
print "total time: ",dt
print "average frequency:", num/dt

motion.stopMove()
tts.say("終わりです。")

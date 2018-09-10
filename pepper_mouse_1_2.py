# -*- coding: utf-8 -*-
"""
Created on 2018/05/ 10:10

pepperマウス操縦のdelayを調べる

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

ip = "192.168.1.69"
port = 9559
localip = "localhost"
localport = 58920

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
# Wake up robot
#motion.wakeUp()

# 自律モードをOFFにする
awareness.stopAwareness()
autoMove.setBackgroundStrategy("none")
autoMove.setExpressiveListeningEnabled(0)
#センサの有効範囲を設定
motion.setOrthogonalSecurityDistance(0.3)
motion.setTangentialSecurityDistance(0.3)
#移動中の腕を固定
motion.setMoveArmsEnabled(False, False)
#腕の衝突保護を設定
motion.setExternalCollisionProtectionEnabled("Arms", False)

#vx0 = 0.0
#vy0 = 0.0

#初期位置を決定
#locallization.learnHome()
#p0 = locallization.getRobotPosition(True)
#px = {}
#py = {}

#px[0] = p0[0]
#py[0] = p0[1]


x = {}  #mouse x
y = {}  #mouse y

motion.setAngles(["LShoulderPitch", "LElbowYaw"], [0.5, 0.5], 0.1)
motion.setAngles(["RShoulderPitch", "RElbowYaw"], [0.5, 0.5], 0.1)
tts.say("ボタンを押してください")
k = raw_input('plz press the key"s": ')
if k == "s\r":
    x0, y0 = pyautogui.position()
    x[0] = x0
    y[0] = y0
else:
    print "no input"
    exit()

tts.say("始まります")

t0 = time.clock()
MaxAccXY = 0.55
MaxVelXY = 0.275
#motion.moveToward(vx0, vy0, 0.0,  [["MaxAccXY", MaxAccXY],["MaxVelXY", MaxVelXY]])

vx = {}  #pepper command velocity calculated by mouse position
vy = {}  #pepper command velocity calculated by mouse position
vx[0] = 0
vy[0] = 0

#vmx = {}  #mouse velocity
#vmy = {}  #mouse velocuty
#vmx[0] = 0
#vmy[0] = 0

pvx = {}  #pepper velocity
pvy = {}  #pepper velocuty
pvx[0] = 0
pvy[0] = 0

t = {}
t[0] = time.clock() - t0
dt = 0.2  #時間間隔設定　refresh rate=50Hz


try:
    i = 1
    while 1:
        t[i] = time.clock() - t0
        #result = motion.getRobotVelocity()
        #p = locallization.getRobotPosition(True)
        #pvx[i] = result[0]
        #pvy[i] = result[1]
        #px[i] = p[0]
        #py[i] = p[1]
        posx, posy = pyautogui.position()
        x[i] = posx
        y[i] = posy
        #vmx[i] = (x[i] - x[i - 1]) / 25.5
        #vmy[i] = (y[i] - y[i - 1]) / 25.5

        vecx = +(y[i] - y[i - 1]) / 25.5
        vecy = +(x[i] - x[i - 1]) / 25.5
        if vecx >= 1.0 or vecx <= -1.0:
            vecx = vecx / abs(vecx)
        if vecy >= 1.0 or vecy <= -1.0:
            vecy = vecy / abs(vecy)
        vx[i] = vecx
        vy[i] = vecy
        motion.moveToward(vx[i], vy[i], 0.0, [["MaxVelXY", MaxVelXY],["MaxAccXY", MaxAccXY]])
        time.sleep(dt)
        i += 1
except KeyboardInterrupt:
    motion.stopMove()

#motion.stopMove()
tts.say("終わりです。")
print "end"
#基本姿勢
posture.goToPosture("StandInit", 0.5)

matrix = np.zeros((len(t), 8))
for i in range(len(t)):
    matrix[i, 0] = i
    matrix[i, 1] = t[i]
    matrix[i, 2] = x[i]
    matrix[i, 3] = y[i]
    matrix[i, 4] = vx[i]
    matrix[i, 5] = vy[i]
    #matrix[i, 6] = px[i]
    #matrix[i, 7] = py[i]
    matrix[i, 8] = pvx[i]
    matrix[i, 9] = pvy[i]

#print matrix
#csvファイルへ書き込み
now = datetime.datetime.now()
filename = "pepper_mouse_" + now.strftime("%Y%m%d%H%M") + ".csv"
np.savetxt(filename, matrix, delimiter=',')

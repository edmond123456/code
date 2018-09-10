# -*- coding: utf-8 -*-
"""
Created on 2018/05/28

test19-21  max velocity=0.1375 0.275 0.55 acc=0.55m/s^2

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

sys.stdout.flush()
ip = "192.168.1.174"
port = 9559
localip = "localhost"
localport = 50371

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
motion.wakeUp()

# 自律モードをOFFにする
awareness.stopAwareness()
autoMove.setBackgroundStrategy("none")
autoMove.setExpressiveListeningEnabled(0)
#センサの有効範囲を設定
motion.setOrthogonalSecurityDistance(0.1)
motion.setTangentialSecurityDistance(0.1)
#移動中の腕を固定
motion.setMoveArmsEnabled(False, False)
#腕の衝突保護を設定
motion.setExternalCollisionProtectionEnabled("Arms", False)

sys.stdout.flush()
vx0 = 0.1
vy0 = 0.0
MaxAccXY = 0.55
MaxVelXY = 0.275
#初期位置を決定
locallization.learnHome()
p0 = locallization.getRobotPosition(True)
px = {}
py = {}
#pz = {}
px[0] = p0[0]
py[0] = p0[1]
#pz[0] = p0[2]

tts.say("始まります")

t0 = time.clock()
motion.moveToward(vx0, vy0, 0.0)

x0, y0 = pyautogui.position()
x = {}  #mouse x
y = {}  #mouse y
x[0] = x0
y[0] = y0

vx = {}  #pepper command velocity calculated by mouse position
vy = {}  #pepper command velocity calculated by mouse position
vx[0] = vx0
vy[0] = vy0

vmx = {}  #mouse velocity
vmy = {}  #mouse velocuty
vmx[0] = 0
vmy[0] = 0
vecx = {}  #mouse velocity
vecy = {}  #mouse velocuty
vecx[0] = 0
vecy[0] = 0

pvx = {}  #pepper velocity
pvy = {}  #pepper velocuty
pvx[0] = 0
pvy[0] = 0

t = {}
t[0] = time.clock() - t0
#dt = 0.125  #時間間隔設定　refresh rate=8Hz
time.sleep(0.05)

i = 1
while 1:
    t[i] = time.clock() - t0
    result = motion.getRobotVelocity()
    p = locallization.getRobotPosition(True)
    pvx[i] = result[0]
    pvy[i] = result[1]
    px[i] = p[0]
    py[i] = p[1]

    posx, posy = pyautogui.position()
    x[i] = posx
    y[i] = posy
    vmx[i] = (x[i] - x[i - 1]) / 25.5
    vmy[i] = (y[i] - y[i - 1]) / 25.5

    vecx = -(y[i] - y[i - 1]) / 25.5
    vecy = -(x[i] - x[i - 1]) / 25.5
    #if abs(vecx) >= 1.0:
    #    vecx = vecx / abs(vecx)
    #if abs(vecy) >= 1.0:
    #    vecy = vecy / abs(vecy)
    if abs(vecx) < 0.1:
        vecx = 0
    if abs(vecy) < 0.1:
        vecy = 0
    if abs(vecx) > 0.3:
        vecx = vecx / abs(vecx)
    if abs(vecy) > 0.3:
        vecy = vecy / abs(vecy)
    if abs(vecx+vecy)>0.1:
        vx[i] = vecx
        vy[i] = vecy
        motion.moveToward(vx[i], vy[i], 0.0,
                      [["MaxVelXY", MaxVelXY], ["MaxAccXY", MaxAccXY]])
    else:
        vx[i]=0
        vy[i]=0
        motion.stopmove()


    sys.stdout.flush()
    i += 1
    if i > 200:
        break

motion.stopMove()
tts.say("終わりです。")
#基本姿勢
posture.goToPosture("StandInit", 0.5)

matrix = np.zeros((len(t), 12))
for i in range(len(t)):
    matrix[i, 0] = i
    matrix[i, 1] = t[i]
    matrix[i, 2] = x[i]
    matrix[i, 3] = y[i]
    matrix[i, 4] = vmx[i]
    matrix[i, 5] = vmy[i]
    matrix[i, 6] = px[i]
    matrix[i, 7] = py[i]
    matrix[i, 8] = pvx[i]
    matrix[i, 9] = pvy[i]
    matrix[i, 10] = vx[i]
    matrix[i, 11] = vy[i]

#print t[len(t)-1]

#csvファイルへ書き込み
now = datetime.datetime.now()
filename = "pepper_mouse_" + now.strftime("%Y%m%d%H%M") + ".csv"
np.savetxt(filename, matrix, delimiter=',')
"""

 test10には8Hzで位置と速度を取ることができた(すべての時刻でデータを取る)

@author: Hua
"""
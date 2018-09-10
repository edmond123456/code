# -*- coding: utf-8 -*-
"""
Created on 2018/05/23

 mouse pepper 速度　位置　時刻

 問題ありそう　放棄
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
#motion.wakeUp()

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

vx0 = 0.1
vy0 = 0.0
MaxAccXY = 0.55
MaxVelXY = 0.35
#初期位置を決定
locallization.learnHome()
p0 = locallization.getRobotPosition(True)
px = {}
py = {}
pz = {}
px[0] = p0[0]
py[0] = p0[1]
pz[0] = p0[2]

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

pvx = {}  #pepper velocity
pvy = {}  #pepper velocuty
pvx[0] = 0
pvy[0] = 0

t = {}
t[0] = time.clock() - t0
dt = 0.006  #時間間隔設定　refresh rate=166Hz
time.sleep(0.1)

i = 1
try:
    while 1:
        posx, posy = pyautogui.position()
        x[i] = posx
        y[i] = posy
        vmx[i] = (x[i] - x[i - 1]) / dt
        vmy[i] = (y[i] - y[i - 1]) / dt
        vecx = -(y[i] - y[i - 1]) / 20.0
        vecy = -(x[i] - x[i - 1]) / 20.0
        if vecx >= 1.0 or vecx <= -1.0:
            vecx = vecx / abs(vecx)
        if vecy >= 1.0 or vecy <= -1.0:
            vecy = vecy / abs(vecy)
        vx[i] = vecx
        vy[i] = vecy
        #print time.clock() - t0
        motion.moveToward(vx[i], vy[i], 0.0)
        #sys.stdout.flush()
        #print time.clock() - t0
        #sys.stdout.flush()
        #if i % 10 == 0:
        result = motion.getRobotVelocity()
        p = locallization.getRobotPosition(True)
        pvx[i] = result[0]
        pvy[i] = result[1]
        px[i] = p[0]
        py[i] = p[1]
        #else:
        #    pvx[i] = 0
        #    pvy[i] = 0
        #    px[i] = 0
        #    py[i] = 0
        #sys.stdout.flush()
        print time.clock() - t0
        #sys.stdout.flush()
        #t[i] = time.clock() - t0
        #time.sleep(dt)
        i += 1
        if i > 50:
            break
except IOError:
    motion.stopMove()
    print "IOError"

    

motion.stopMove()
tts.say("終わりです。")
#基本姿勢に戻る
posture.goToPosture("StandInit", 0.5)

#matrix = np.zeros((len(t), 10))
#for i in range(len(t)):
#    matrix[i, 0] = i
#    matrix[i, 1] = t[i]
#    matrix[i, 2] = x[i]
#    matrix[i, 3] = y[i]
#    matrix[i, 4] = vmx[i]
#    matrix[i, 5] = vmy[i]
#    matrix[i, 6] = px[i]
#    matrix[i, 7] = py[i]
#    matrix[i, 8] = pvx[i]
#    matrix[i, 9] = pvy[i]

#print matrix
#print t[len(t) - 1]


#csvファイルへ書き込み
#now = datetime.datetime.now()
#filename = "pepper_mouse_" + now.strftime("%Y%m%d%H%M%S") + ".csv"
#np.savetxt(filename, matrix, delimiter=',')

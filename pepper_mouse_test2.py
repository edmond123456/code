# -*- coding: utf-8 -*-
"""
Created on 2018/05/16

pepperをずっと動かせたい
pepperがずっと動いているが、方向が常に変化する

pepper velocity <=0.56m/s  速度換算式 v=0.326*k(-1<k<1)
GOAL: delay<0.2s
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

ip = "192.168.1.174"
port = 9559
localip = "localhost"
localport = 57822

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
motion.setOrthogonalSecurityDistance(0.0)
motion.setTangentialSecurityDistance(0.01)
#移動中の腕を固定
motion.setMoveArmsEnabled(False, False)
#腕の衝突保護を設定
motion.setExternalCollisionProtectionEnabled("Arms", False)

tts.say("始まります")
vx = 0.3
vy = 0.0
theta = 0.0
motion.moveToward(vx, vy, theta)
x0, y0 = pyautogui.position()
x = {}  #mouse x
y = {}  #mouse y
x[0] = x0
y[0] = y0
vx = {}  #mouse x
vy = {}  #mouse y
vx[0] = vx
vy[0] = vy
px = {}  # pepper path
py = {}  # pepper path
px[0] = 0.0
py[0] = 0.0
dt = 0.006  #時間間隔設定　refresh
time.sleep(1)


i = 1
while 1:
    posx, posy = pyautogui.position()
    x[i] = round(posx, 2)
    y[i] = round(posy, 2)
    vecx = -(y[i] - y[i - 1]) / 30.0
    vecy = -(x[i] - x[i - 1]) / 30.0
    if vecx >= 1.0 or vecx <= -1.0:
        vecx = vecx / abs(vecx)
    if vecy >= 1.0 or vecy <= -1.0:
        vecy = vecy / abs(vecy)
    #if x[i] == 0 or x[i] == 1920 or y[i] == 0 or y[i] == 1080:
    #    vecx = vx[i - 1]
    #    vecy = vy[i - 1]
    vx[i] = vecx
    vy[i] = vecy
    motion.moveToward(vx[i], vy[i], theta)
    time.sleep(dt)
    px[i] = px[i - 1] + vx[i] * dt
    py[i] = py[i - 1] + vy[i] * dt
    i += 1
    if i > 1000:
        break

motion.stopMove()
tts.say("終わりです。")

#print x,y,vx,vy,px,py
#print len(x),len(y),len(vx),len(vy),len(px),len(py)

#print vx
#print vy
#print len(vx)

matrix = np.zeros((len(x), 4))
for i in range(len(x)):
    matrix[i, 0] = x[i]  #mouse  left&right
    matrix[i, 1] = y[i]  #mouse  front&back
    #matrix[i, 2] = vx[i]  #pepper left&right velocity
    #matrix[i, 3] = vy[i]  #pepper front&back velocity
    matrix[i, 2] = px[i]  # pepper left&right path
    matrix[i, 3] = py[i]  #pepper front&back path

#print matrix
#print len(matrix)  # 配列の行数

# csvファイルへの書き出し
#fileHeader = ["mouse_x", "mouse_y", "pepper_frontback", "pepper_leftright"]
#csvFile = open("pepper_mouse.csv", "wb")
#writer = csv.writer(csvFile)
#writer.writerow(fileHeader)

np.savetxt('pepper_mouse_test21.csv', matrix, delimiter=',')

#csvFile.close()
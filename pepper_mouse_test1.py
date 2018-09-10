# -*- coding: utf-8 -*-
"""
Created on 2018/05/16

古川：2018/05/16 15:58  
以下のグラフを重ねてください． 
・マウスの入力軌跡（マウス座標の取得とCSVへの書き出しをしてください） 
・Pepperの移動軌跡（外部カメラでの計測ではなく推定位置）

pepper velocity <=0.56m/s
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
localport = 64355

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
    awareness = ALProxy("ALBasicAwareness", localip, localport)
    autoMove = ALProxy("ALAutonomousMoves", localip, localport)
else:
    print "no input"
    exit()

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

#基本姿勢
posture.goToPosture("StandInit", 0.5)
#motion.wakeUp()
# motion.setAngles(["HeadYaw", "HeadPitch"], [0.0, 0.0], 0.1)

# void ALMotionProxy::setAngles(names,angles,fractionMaxSpeed)
#motion.setAngles(["LShoulderPitch", "LShoulderRoll"], [1.0, 0.0], 0.1)

#motion.moveTo(0.3,0.0,-math.pi/2)
#motion.moveTo(-1.3,0.0,0.0)
#motion.moveTo(0.9,0.0,0.0)
tts.say("始まります")
x0, y0 = pyautogui.position()
listx = {}  #mouse x
listy = {}  #mouse y
listdx = {}  # pepper move cammand
listdy = {}  # pepper move cammand
listpx = {}  # pepper path
listpy = {}  # pepper path
listx[0] = x0
listy[0] = y0
listdx[0] = 0
listdy[0] = 0
listpx[0] = 0
listpy[0] = 0
time.sleep(3)

for i in range(1, 21):
    x, y = pyautogui.position()
    listx[i] = x
    listy[i] = y
    dx = -(listx[i] - listx[i - 1]) * 0.003  #-1.88~1.88m　xが大きくなるなら、右へ
    dy = -(listy[i] - listy[i - 1]) * 0.003  #-1.08~1.08m yが小さくなるなら、前進
    listdx[i] = dx  #pepper 左右　dx
    listdy[i] = dy
    listpx[i] = listpx[i - 1] + dx
    listpy[i] = listpy[i - 1] + dy
    motion.moveTo(dy, dx, 0.0)  #pepperの向いている方向はx軸

    #sys.stdout.flush()
    time.sleep(3)

tts.say("終わりです。")
# motion.rest()

matrix = np.zeros((len(listx), 6))
for i in range(len(listx)):
    matrix[i, 0] = listx[i]  #mouse  left&right
    matrix[i, 1] = listy[i]  #mouse  front&back
    matrix[i, 2] = listdx[i]  #pepper left&right
    matrix[i, 3] = listdy[i]  #pepper front&back
    matrix[i, 4] = listpx[i]  # pepper left&right path
    matrix[i, 5] = listpy[i]  #pepper front&back path

#print matrix
#print len(matrix)  # 配列の行数

# csvファイルへの書き出し
#fileHeader = ["mouse_x", "mouse_y", "pepper_frontback", "pepper_leftright"]
#csvFile = open("pepper_mouse.csv", "wb")
#writer = csv.writer(csvFile)
#writer.writerow(fileHeader)

#np.savetxt('pepper_mouse_test1.csv', matrix, delimiter=',')

#csvFile.close()
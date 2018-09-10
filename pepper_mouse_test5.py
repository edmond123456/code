# -*- coding: utf-8 -*-
"""
Created on 2018/05/21

   ALMotion pepperの速度変化にはどれくらいの時間がかかる？
pepperの推定位置、速度ではなく、実際の位置、速度
pepper velocity <=0.56m/s  速度換算式 v=0.326*k(-1<k<1)

@author: Hua
"""


from naoqi import ALProxy
import time
from multiprocessing import Process
import math
import numpy as np
import almath
import sys
import pyautogui
import csv

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

def initialization():
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
    vx0 = 0.1
    vy0 = 0.0
    #初期位置を決定
    #locallization.learnHome()
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
    time.sleep(0.3)  



def motor(i):
    posx, posy = pyautogui.position()
    x[i] = posx
    y[i] = posy
    vmx[i] = (x[i] - x[i - 1]) / dt
    vmy[i] = (y[i] - y[i - 1]) / dt

    vecx = -(y[i] - y[i - 1]) / 15.0
    vecy = -(x[i] - x[i - 1]) / 15.0
    if vecx >= 1.0 or vecx <= -1.0:
        vecx = vecx / abs(vecx)
    if vecy >= 1.0 or vecy <= -1.0:
        vecy = vecy / abs(vecy)
    vx[i] = vecx
    vy[i] = vecy
    motion.moveToward(vx[i], vy[i], 0.0)




def sensor(i):
    result = motion.getRobotVelocity()
    p = locallization.getRobotPosition(True)
    pvx[i] = result[0]
    pvy[i] = result[1]
    px[i] = p[0]
    py[i] = p[1]
    t[i] = time.clock() - t0

if __name__ == '__main__':
    initialization()
    for i in range(100):
        p1=Process(target=motor,args=(i))
        p2=Process(target=sensor,args=(i))
        p1.start()
        p2.start()
        #p1.join()
        #p2.join()
    




"""
Created on 2018/05/21

motion.moveToward(1.0,0.0,0.0)
time.sleep(3.0)
motion.stopMove()
pepperは最大速度で3秒走るではない
pepperはちょうど3秒後止まる

@author: Hua
"""
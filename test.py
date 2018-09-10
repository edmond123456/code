# -*- coding: utf-8 -*-
"""
Created on 2018/05/16 pepperの動き精度テスト

@author: Hua

pepper 最大速度 0.55m/s

test1
"""

#test
from naoqi import ALProxy
import time
import math
import numpy as np
import almath
import sys
import pyautogui

ip = "192.168.1.69"
port = 9559
localip = "localhost"
localport = 53219

#g = raw_input('select the robot(1:pepper, 2:virtual robot): ')
g = "1\r"
if g == "1\r":
    motion = ALProxy("ALMotion", ip, port)
    posture = ALProxy("ALRobotPosture", ip, port)
    #locallization = ALProxy("ALLocalization", ip, port)
    tts = ALProxy("ALTextToSpeech", ip, port)
    #awareness = ALProxy("ALBasicAwareness", ip, port)
    #autoMove = ALProxy("ALAutonomousMoves", ip, port)
    postureProxy = ALProxy("ALRobotPosture", ip, port)

elif g == "2\r":
    motion = ALProxy("ALMotion", localip, localport)
    posture = ALProxy("ALRobotPosture", localip, localport)
    #locallization = ALProxy("ALLocalization", localip, localport)
    tts = ALProxy("ALTextToSpeech", localip, localport)
    #awareness = ALProxy("ALBasicAwareness", localip, localport)
    #autoMove = ALProxy("ALAutonomousMoves", localip, localport)
    postureProxy = ALProxy("ALRobotPosture", localip, localport)
else:
    print "no input"
    exit()


#センサの有効範囲を設定
motion.setOrthogonalSecurityDistance(0.0)
motion.setTangentialSecurityDistance(0.01)
#移動中の腕を固定
motion.setMoveArmsEnabled(False, False)
#腕の衝突保護を設定
motion.setExternalCollisionProtectionEnabled("Arms", False)





#motion.wakeUp()
# Send robot to Pose Init
#postureProxy.goToPosture("StandInit", 0.5)
# motion.setAngles(["HeadYaw", "HeadPitch"], [0.0, 0.0], 0.1)

# void ALMotionProxy::setAngles(names,angles,fractionMaxSpeed)
#motion.setAngles(["LShoulderPitch", "LShoulderRoll"], [1.0, 0.0], 0.1)



# 前進0.3m
#useSensorValues = False
#initRobotPosition = almath.Pose2D(motion.getRobotPosition(useSensorValues))

# Make the robot move
#motion.moveTo(0.3, 0.0, 0.0)




#前後0.5m繰り返し10回 補正-6%
#for i in range(10):
#    motion.moveTo(0.5, 0.0, 0.0)
#    motion.moveTo(-0.5*0.94, 0.0, 0.0)

#左右0.5m繰り返し10回 補正6%
#for i in range(1,11):
    #print i
#    motion.moveTo(0.0, 0.5, 0.0)
#    motion.moveTo(0.0, -0.5*1.06, 0.0)


#前後0.3m繰り返し10回 
#for i in range(10):
#    motion.moveTo(0.3, 0.0, 0.0)
    
#    motion.moveTo(-0.3, 0.0, 0.0)

#左右0.3m繰り返し10回 補正-0.02
#for i in range(10):
#    motion.moveTo(0.0, 0.3, 0.0)
#    motion.moveTo(0.0, -0.32, 0.0)


#endRobotPosition = almath.Pose2D(motion.getRobotPosition(useSensorValues))

# Compute robot's' displacement
#robotMove = almath.pose2DInverse(initRobotPosition)*endRobotPosition
#print "Robot Move:", robotMove

#motion.moveTo(0.,0.0,-math.pi)

t0=time.clock()
motion.moveToward(1.0,0.0,0.0)
time.sleep(1)
print time.clock()-t0
motion.stopMove()
#motion.moveTo(0.9,0.0,0.0)

#motion.rest()

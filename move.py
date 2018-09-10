# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 13:20:26 2018

@author: Hua
"""

from naoqi import ALProxy
import time
import math
import numpy as np
import almath
import datetime

#バーチャルロボット
ip_v = "localhost"
port_v = 52877

#wifi環境
ip_wifi = "192.168.1.69"
port_wifi = 9559

#l = ALProxy("ALLocalization", "192.168.1.174", 9559)
motion = ALProxy("ALMotion", ip_wifi, port_wifi)
awareness = ALProxy("ALBasicAwareness", ip_wifi, port_wifi)
autoMove = ALProxy("ALAutonomousMoves", ip_wifi, port_wifi)
locallization = ALProxy("ALLocalization", ip_wifi, port_wifi)

useSensorValues = False
#充電座標　[1.27349054813385, 0.37449413537979126, -2.9227664470672607]
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


def main():
    #初期位置を決定
    #locallization.learnHome()
    p0 = locallization.getRobotPosition(True)
    px = {}
    py = {}
    px[0] = p0[0]
    py[0] = p0[1]

    MaxAccXY = 0.55
    MaxVelXY = 0.55
    # Example showing how to use waitUntilMoveIsFinished.
    # Start a walk
    x = 0.0
    y = -1.0
    theta = math.pi
    motion.moveToward(x, y, 0.0,
                      [["MaxAccXY", MaxAccXY], ["MaxVelXY", MaxVelXY]])
    #motion.moveToward(x, y, theta,
    #                  [ ["MaxVelXY", MaxVelXY]])
    #motion.moveToward(x, y, theta,
    #                  [["MaxAccXY", MaxAccXY]])
    #motion.moveTo(x, y, theta)

    # Wait for it to finish
    #motion.waitUntilMoveIsFinished()
    # Then do something else
    time.sleep(1.5)
    motion.stopMove()
    #motion.killMove()  #約20ms
    p = locallization.getRobotPosition(True)
    px[1] = p[0]
    py[1] = p[1]
    matrix = np.zeros((len(px), 2))
    for i in range(len(px)):
        matrix[i, 0] = px[i]
        matrix[i, 1] = py[i]
    #csvファイルへ書き込み
    #now = datetime.datetime.now()
    #filename = "pepper_mouse_" + now.strftime("%Y%m%d%H%M") + ".csv"
    #np.savetxt(filename, matrix, delimiter=',')
    motion.setAngles(["RShoulderPitch", "RElbowYaw"], [1.5, 1.5], 0.1)
    motion.setAngles(["LShoulderPitch", "LElbowYaw"], [1.5, 1.5], 0.1)



if __name__ == "__main__":
    main()

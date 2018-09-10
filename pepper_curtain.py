# -*- coding: utf-8 -*-
"""
Created on Tue May 30 20:51:40 2017

@author: miwa
"""

from naoqi import ALProxy
import time
import datetime
import math
import getch
import numpy as np
import postures as pos
import winsound as ws
import csv
import ctypes
import ctypes.wintypes
#import shmem

#akiyama 20170125
#import shmem

IP = "192.168.1.68"
PORT = 9559
localIP = "localhost"
localPORT = 62269
Pi = math.radians(180)
r0 = 0.15   #回転軸から肩までの長さ
r1 = 0.181 #肩から肘までの長さ
r2 = 0.22   #肘から手のひらまでの長さ

jointnames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand",
              "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand",
              "HeadPitch", "HeadYaw", "HipPitch", "HipRoll"]

timelog = ["time"]
countlog = ["counter"]
freqlog = ["freq"]
commandlog = ["command"]
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

#akiyama 20170125
#C++mainconsoleを立ち上げてから
#DB = shmem.Shmem(True)
delay = 0.2
g = getch._Getch()
#実機かバーチャルロボットか選択
print("1:robot, 2:virtual robot")
x = g()
#x = 2

if(str(x) == "1"):
    m = ALProxy("ALMotion", IP, PORT)
    p = ALProxy("ALRobotPosture", IP, PORT)
    l = ALProxy("ALLocalization", IP, PORT)
    tts = ALProxy("ALTextToSpeech", IP, PORT)
else:
    m = ALProxy("ALMotion", localIP, localPORT)
    p = ALProxy("ALRobotPosture", localIP, localPORT)
    l = ALProxy("ALLocalization", localIP, localPORT)
    tts = ALProxy("ALTextToSpeech", localIP, localPORT)

def TransMatrixFun(worldX,worldY,GapTheta,GapX,GapY):
    WorldMatrix = np.matrix([[worldX],[worldY],[1]])
    TransMatrix = np.matrix([[math.cos(GapTheta), math.sin(GapTheta), GapX],[-math.sin(GapTheta), math.cos(GapTheta), GapY],[0, 0, 1]])
    PepperMatrix = WorldMatrix * TransMatrix
    print "PepperMatrix:", PepperMatrix

def MeasureTheta(PosTheta):   #pepperの進行方向を求める関数.radで返す。
    #homeposとmoveToward後のposの差でθを求める。
    #thetaを求める為にレーザー発射姿勢よーし！
    m.setAngles(jointnames, pos.b2, 0.2)
    print"**********************************************************"
    print"Show command  2:uno'clock, 5:stop, 8:o'clock, 0:Next"
    #2で反時計回り,8で時計回りに回転する。5でストップ。0でtheta0を決定して次のレーザーに移行する。
    while(1):
        x = g()
        if(str(x) == "2"):
            print x
            m.moveToward(0.0, 0.0, 0.1)
            #m.setAngles(jointnames, pos.b2, 0.2)

        elif(str(x) == "5"):
            print x
            m.moveToward(0.0, 0.0, 0.0)
            m.setAngles(jointnames, pos.b2, 0.2)

        elif(str(x) == "8"):
            print x
            m.moveToward(0.0, 0.0, -0.1)
            #m.setAngles(jointnames, pos.b2, 0.2)

        elif(str(x)=="0"):
            print("Next")
            m.moveToward(0.0, 0.0, 0.0)
            posAfter = l.getRobotPosition(True)
            print "posAfter:", posAfter
            theta = (posAfter[2] - PosTheta)
            break

        else:
            print "no input", x
            #m.setAngles(jointnames, pos.b2, 0.2)

    return theta


#この関数を起動するとペッパーの横レーザーが動き、ペッパーの手の中心からレーザーを止めた位置までの直線距離が求める。
#ペッパーからのx軸方向の距離を返す(xは縦方向である事に注意)。
def MeasureDistance(WristTheta, num):
    m.setAngles(jointnames, pos.b2, 0.1)
    time.sleep(2.0)
    m.setAngles([jointnames[8], jointnames[10]], [0.0, WristTheta], 0.2)
    print "****************************************************************"
    print "Show command  2:laser down, 5:laser stop, 8:laser up, 0:Go"
    phi = 100
    while(1):
        x = g()
        if(str(x) == "2"):
            print "down"
            if(num == 1):   #numによって手首の回る速さが変わる
                m.setAngles(jointnames[10], 1.5, 0.01)
            elif(num == 2):
                m.setAngles(jointnames[10], 1.5, 0.01)

        elif(str(x) == "5"):
            print "stop"
            phi = m.getAngles(jointnames[10], False)[0]
            m.setAngles(jointnames[10], phi, 0.5)

            if(num == 1):    #スタート位置からカーテンの前までの距離を測る場合
                DisToCurtain = 0.9*math.tan(math.radians(90-phi*60))
            elif(num == 2):  #カーテンの前で掴む位置をまでの距離を測る場合
                DisToCurtain = (0.15+(0.07-0.07*math.cos(math.radians(abs(phi)*60))))/math.tan(math.radians(abs(phi)*60)) - 0.07*math.sin(math.radians(abs(phi)*60)) + 0.1

            print "phi:", phi
            print "DisToCurtain:", DisToCurtain

        elif(str(x) == "8"):
            print "Up"
            if(num == 1):   #numによって手首の回る速さが変わる
                m.setAngles(jointnames[10], -1.5, 0.01)
            elif(num == 2):
                m.setAngles(jointnames[10], -1.5, 0.01)

        elif(str(x) == "0"):    #出発する
            if(phi == 100): #phiが決定していない場合はループを抜けない
                continue

            print "Go"
            #tts.say("いってきますね")
            break

        else:
            print x, "no input"

    #握った手の中心からカーテンまでの距離を求めてる。
    #肘を曲げているので、ペッパーの動く中心からs(=0.21m)離れている事に注意。
    #DisToCurtain = (0.25+(0.07-0.07*math.cos(math.radians(abs(phi)*60))))/math.tan(math.radians(abs(phi)*60)) - 0.07*math.sin(math.radians(abs(phi)*60)) + 0.1
    #DisToCurtainに10cmの誤差修正を加えた
    print "phi:", phi
    print "DisToCurtain:", DisToCurtain,"[m]"
    return DisToCurtain

##################腕を伸ばすときに使う関数###############################
def Reaching(Dis):
    StoH = math.sqrt(r1*r1 + r2*r2)    #SRが90度の時の肩と手の距離
    print "StoH", StoH

    #手が届かない場合，手が届く距離まで近づく
    Dis3 = 0
    if(Dis > 0.4):
        Dis3 = Dis - 0.4
        print "Dis3:", Dis3
        m.moveTo(Dis3 + Dis*0.2, 0.0, 0.0, 0.5)
        Dis = 0.4

    elif(Dis < StoH):
        Dis3 = Dis - 0.4
        print "Dis3:", Dis3
        m.moveTo(-Dis3, 0.0, 0.0, 0.5)
        Dis = 0.4

    #腕をDisToCurtain伸ばすのに必要なElboeRollの角度を計算
    theta4 = math.acos((r1*r1 + r2*r2 - (Dis)*(Dis))/(2*r1*r2))
    ERtheta = (180 - math.degrees(theta4))/60   #ElbowpRollに入力する形に変換
    print "ERtheta:", ERtheta

    #手の高さを一定に保つのに必要なSholderPitchの角度を計算
    theta5 = math.acos((r1*r1 + (Dis)*(Dis) - r2*r2)/(2*r1*(Dis)))
    SPtheta = (math.degrees(theta5)-10)/60      #SholderPitchに入力する形に変換
    print "SPtheta:", SPtheta

    #腕をカーテンと垂直にする。横からカーテンの裾を掴むイメージ。
    m.setAngles(jointnames[7],-0.3,0.2)
    time.sleep(0.5)
    m.setAngles([jointnames[6], jointnames[9], jointnames[11]], [SPtheta, ERtheta, 1.0], 0.2)
    time.sleep(0.5)
    m.setAngles([jointnames[7], jointnames[10]], [0.0, -0.2], 0.05)
    time.sleep(2.5)
    m.setAngles(jointnames[11], 0.0, 0.1)

######################ここからメイン関数###########################
def curtain():


    #(1)---------------カーテンの近くまで移動する---------------------------------
    #theta0 = MeasureTheta(homepos[2])

    #DisToCurtain = MeasureDistance(1.2, 1)

    #m. moveTo(DisToCurtain, 0.0, 0.0, 8.0)

    #m.moveTo(0.0, 0.0, Pi/2 - theta0)
    
    m.moveTo(1.0, 0.0, 0.0, 5.0)
    time.sleep(2.0)
    
    m.moveTo(0.0, 0.0, Pi/2, 3.0)
    
    m.moveTo(0.3, 0.0, 0.0, 3.0)

    position = l.getRobotPosition(True)
    print " position:", position

    #------------------掴みに行くカーテンの端までの方向と距離を測る-----------------
    print "Please shine a laser to curtain that you wanna catch."
    theta1 = MeasureTheta(position[2])
    print "theta1:", theta1, "[rad]"

    Dis1 = MeasureDistance(0.0, 2)
    #誤差を打ち消す三平方の定理
    Dis1 = math.sqrt((Dis1+r1)**2+(r0 + 0.05)**2)
    print "Dis1:", Dis1,"[m]"

    #---------------------反対側のカーテンの端までの向きと距離を測る----------------------
    position = l.getRobotPosition(True)
    print "position:", position

    theta2 = MeasureTheta(position[2])
    print "theta2:", theta2, "[rad]"

    print "Please shine a laser to end of curtain."
    Dis2 = MeasureDistance(0.0, 2)
    #誤差を消す三平方の定理
    Dis2 = math.sqrt((Dis2+r1)**2+(r0 + 0.05)**2)
    print "Dis2:", Dis2,"[m]"

    #theta2の誤差を無くす計算。
    theta2 = theta2 - math.acos(r1/Dis1) + math.acos(r1/Dis2)
    print "Re:theta2:",theta2

    #----------------theta1,theta2,Dis1,Dis2を使ってpepperをカーテンに正対させる-------------------------
    """
    Dis3:掴む側のカーテンの端から反対側のカーテンの端までの距離
    alpha:カーテンとDis1がなす角度
    beta:カーテンとDis2がなす角度（ここでは使わないので計算していない）
    l1:pepperの位置からカーテンまでの距離
    l2:pepperの位置からつかむカーテンの端までカーテンと平行な方向に移動する距離
    theta3:掴むのと反対側のカーテンの端の方向からカーテンに正対する方向までの角度
    """

    Dis3 = math.sqrt(Dis1*Dis1 + Dis2*Dis2 - 2*Dis1*Dis2*math.cos(theta2))
    print "|*****************|"
    print "Dis1:",Dis1,"[m]"
    print "Dis2:",Dis2,"[m]"
    print "Dis3:", Dis3,"[m]"
    print"in () of acos:",((Dis1*Dis1 + Dis3*Dis3 - Dis2*Dis2)/(2*Dis1*Dis3))

    Alpha = math.acos((Dis1*Dis1 + Dis3*Dis3 - Dis2*Dis2)/(2*Dis1*Dis3))
    print "Alpha:", Alpha, "[rad]"

    l1 = Dis1 * math.sin(Alpha)
    print "l1:", l1,"[m]"

    l2 = Dis1 * math.cos(Alpha)
    print "l2:", l2,"[m]"

    theta3 = theta2 - (Pi/2 - Alpha)
    print "theta3:", theta3, "[rad]"


    #（４）---------------------つかむ態勢をとる．-------------------------------
    m.setAngles(jointnames, pos.Rsearch_curtain, 0.2)
    time.sleep(1.0)

    m.moveTo(0.0, 0.0, -theta3 - 4.5*(Pi/180), 2.0)   #3度分多く回してる
    pos1 = l.getRobotPosition(True)
    print"pos1[2]:" , pos1[2]
    time.sleep(1.0)
    m.moveTo(0.0,-l2+r0 + 0.05, 0.0, 2.0)
    time.sleep(2.0)

    #l1m先にあるカーテンの裾を掴む
    Reaching(l1)
    
    position = l.getRobotPosition(True)
    print " position:", position

    """
    #もし取れなかった場合のやり直し
    print "If pepper cannot catch the curtain, please push [r]."
    print "If pepper catched the curtain, please push [s]."
    x = g()
    if(str(x) == "r"):
        print x
        m.moveTo(-0.15,0,0,1.0)
        time.sleep(1.0)
        m.setAngles(jointnames[11],1.0,0.5)
        time.sleep(0.75)
        DisToCurtain = MeasureDistance(0.0,2) + r1
        #Reaching()を使う際はMeasureDistance()にr1を足すのを忘れない事。
        m.setAngles(jointnames, pos.Rsearch_curtain, 0.2)
        time.sleep(1.3)
        Reaching(DisToCurtain)
    if(str(x) == "s"):
        print x
    """

    #(7)-----開けるか閉めるかを選択する。
    while(1):
        print "4:left 5:stop 6:right 0:finish"
        x = g()
        if(str(x) == "4"):
            print "left"
            #m.moveToward(0.0, 0.3, 0.0)
            m.moveTo(0.0, 0.6, 0.0, 5.0)

        elif(str(x) == "5"):
            print "stop"
            m.moveToward(0.0, 0.0, 0.0)

        elif(str(x) == "6"):
            #カーテンを掴んで横移動
            print "right"
            #m.moveToward(0.0, -0.3, 0.0)
            m.moveTo(0.0, -0.6, 0.0, 5.0)

        elif(str(x) == "0"):
            print "finish"
            break

        else:
            print "no input", x

    time.sleep(1.0)

    #------------------カーテンから手を放す-----------------------------
    m.setAngles([jointnames[7], jointnames[11]], [-0.1, 1.0], 0.05)
    time.sleep(0.5)

    #カーテンの裾を引きずらないように下げる。
    m.setAngles(jointnames[7],-0.3,0.2)
    time.sleep(0.7)
    m.moveTo(-0.3,0,0,1.0)
    time.sleep(1.0)
    p.goToPosture("StandInit", 0.5)
    print ("Initialized.....")
    position = l.getRobotPosition(True)
    print " position:", position

    l.goToHome()

    p.goToPosture("StandInit", 0.5)
    m.moveTo(-0.2, 0.0, 0.0)
    print ("Initialized.....")
    position = l.getRobotPosition(True)
    print " position:", position


    
    
    
    
    
    
    
    
    
    
    
    
    
    

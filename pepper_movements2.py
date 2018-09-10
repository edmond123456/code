# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 12:49:58 2017

@author: Raparo_A
"""

from naoqi import ALProxy
import time
import datetime
import math
import getch
import postures as pos
import winsound as ws
import csv
import ctypes
import ctypes.wintypes
#import shmem

#akiyama 20170125
#import shmem

IP = "192.168.2.100"
PORT = 9559
localIP = "localhost"
localPORT = 63827
Pi = math.radians(180)

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

m = ALProxy("ALMotion", IP, PORT)
p = ALProxy("ALRobotPosture", IP, PORT)
l = ALProxy("ALLocalization", IP, PORT)
tts = ALProxy("ALTextToSpeech", IP, PORT)

def log(num, t, count, freq):
    timelog.append(t)
    commandlog.append(num)
    countlog.append(count)
    freqlog.append(freq)
    
def timer(num):
    t = time.time()
    count = ctypes.wintypes.LARGE_INTEGER()
    freq = ctypes.wintypes.LARGE_INTEGER()
    kernel32.QueryPerformanceFrequency(ctypes.byref(freq))
    kernel32.QueryPerformanceCounter(ctypes.byref(count))
    num += 1
    #DB.z = num
    log(num, t, count.value, freq.value)
    return num
    
def Shoulder_Reguration(num, theta, t, v):
    #肩を右へ:7
    ws.Beep(1000, 300)
    num = timer(num)
    m.setAngles(jointnames[7], theta, v)
    time.sleep(t)
    
    #肩を左へ:8
    ws.Beep(1000, 300)
    num = timer(num)
    m.setAngles(jointnames[7], 0.0, v)
    time.sleep(t)
    
    #肩を右へ:9
    ws.Beep(1000, 300)
    num = timer(num)
    m.setAngles(jointnames[7], theta, v)
    time.sleep(t)
    
    #手首の調節へ:10
    ws.Beep(1000, 300)
    
    print "theta:", m.getAngles(jointnames[7], False)
    m.setAngles([jointnames[8], jointnames[10]], [0.0, 0.6], 0.2)
    time.sleep(1.0)
    
    return num
    
def Wrist_Reguration(num, theta, t):
    #下から上へ
    m.setAngles(jointnames[10], theta, 0.02)
    time.sleep(t)
    
    #上から下へ:12
    ws.Beep(1000, 300)
    num = timer(num)
    m.setAngles(jointnames[10], 0.6, 0.02)
    time.sleep(t)
    
    #下から上へ:13
    ws.Beep(1000, 300)
    num = timer(num)
    m.setAngles(jointnames[10], theta, 0.02)
    time.sleep(t)
    
    return num

def main():
#    実機かバーチャルロボットか選択
    g = getch._Getch()
#    x = g()
    x = 1
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
    
    #初期位置を決定
    l.learnHome()
    homepos = l.getRobotPosition(True)
    print "homepos:", homepos
    
    #センサの有効範囲を設定
    m.setOrthogonalSecurityDistance(0.0)
    m.setTangentialSecurityDistance(0.01)
    #移動中の腕を固定
    m.setMoveArmsEnabled(False, False)
    #腕の衝突保護を設定
    m.setExternalCollisionProtectionEnabled("Arms", False)
    
    #待機場所へ移動
    """
    m.moveTo(-1.0, -0.5, 0.0)
    waitpos = l.getRobotPosition(True)
    print "waitpos:", waitpos
    """
    
    #基本姿勢
    p.goToPosture("StandInit", 0.5)
    print ("Initialized.")
    
    time.sleep(3.0)
    """
    #sを押すとスタート
    print "Please push s"
    #x = g()
    x = "s"
    if(str(x) == "s"):
        start = time.time()
        log(x, start - start)
        print("start")
    """
    loop = 0
    while(1):
        loop += 1
        
        print "continue:1"
        print "finish:2"
        
        x = g()
        if(str(x) == "1"):
            print "loop:", loop, "round"
            
            print "1:short"
            print "2:middle"
            print "3:long"
            n = g()
            print "n:", n
            
            homepos = l.getRobotPosition(True)
            print "homepos:", homepos
            time.sleep(2.0)
            
            ws.Beep(1000, 300)
            time.sleep(1.0)
            ws.Beep(1000, 300)
            time.sleep(1.0)
            ws.Beep(1000, 700)
            num = -1
            timer(num)
            time.sleep(1.0)
            #計測開始
            
            #左手のマジックハンドを上げる:0
            m.setAngles(jointnames, pos.Lup, 0.2)
            time.sleep(2.0)
    
            print "1:drink"
            print "2:curtain"
            print "3:floor"
            
            #口パク:1
            ws.Beep(1000, 300)
            num = timer(num)
            time.sleep(3.0)
            
            #drink or curtain or floor:2
            ws.Beep(1000, 300)
            num = timer(num)
            #x = g()
            x = 1
            if(str(x) == "1"):
                #机の上のものを取ってくる
                tts.say("ドリンクですね")
                print ("drink")
                time.sleep(2.0)
                """
                #m.moveTo(1.0 - 0.12, 0.5, 0.0)
                position = l.getRobotPosition(True)
                print (l.getRobotPosition(True))
                #l.goToHome()
                position = l.getRobotPosition(True)
                print (l.getRobotPosition(True))
                
                while(1):
                    if(position[0]>0.01 or position[1]>0.01 or position[2]>0.1):
                        m.moveTo(-position[0], -position[1], -position[2])
                        position = l.getRobotPosition(True)
                        print (position)
                    else:
                        break
                """
                #レーザーを床に撃つ:3
                ws.Beep(1000, 300)
                num = timer(num)
                m.setAngles(jointnames, pos.b2, 0.2)
                time.sleep(2.0)
                
                print "1:left", "2:stop", "3:right"
                time.sleep(2.0)
                while(1):
                    x = 4
                    #x = g()
                    if(str(x) == "1"):
                        m.moveToward(0.0, 0.0, 0.1)
                    elif(str(x) == "2"):
                        m.moveToward(0.0, 0.0, 0.0)
                    elif(str(x) == "3"):
                        m.moveToward(0.0, 0.0, -0.1)
                    else:
                        print x
                        tts.say("いってきますね")
                        break
                
                #前進:4
                time.sleep(2.0)
                ws.Beep(1000, 300)
                num = timer(num)
        
                m.setOrthogonalSecurityDistance(0.0)
                
                #移動
                m.moveTo(1.5, 0.0, 0.0, 6.0)
                
                position = l.getRobotPosition(True)
                print "m.moveTo(1.5, 0.0, 0.0, 6.0):", position
                
                m.setOrthogonalSecurityDistance(0.0)
                
                #補正:5
                ws.Beep(1000, 300)
                num = timer(num)
                
                m.moveTo(0.0, 0.0, math.radians(7.25))
                time.sleep(0.5)
                m.moveTo(0.0, 0.07, 0.0)
                position1 = l.getRobotPosition(True)
                print "m.moveTo(0.0, 0.0, math.radians(7.252255)):", position1
                homepos[2] = position1[2]

                #肩調節の姿勢へ:6
                ws.Beep(1000, 300)
                num = timer(num)
                m.setAngles(jointnames, pos.Rsearch_curtain, 0.05)
                
                """
                m.setAngles(jointnames[7], -1.5, 0.02)
                time.sleep(0.7)
                theta1 = m.getAngles(jointnames[7], False)
                m.setAngles(jointnames[7], theta1, 0.2)
                time.sleep(0.5)
                m.setAngles([jointnames[8], jointnames[10]], [0.0, 0.0], 0.2)
                time.sleep(1.5)
                theta2 = m.getAngles(jointnames[10], False)
                """
                
                time.sleep(3.0)
                
                #肩調節
                """
                theta1 = []
                if(n == "1"):
                    theta1.append(-0.27)
                    num = Shoulder_Reguration(num, theta1[0], 2.0, 0.05)
                elif(n == "2"):
                    theta1.append(-0.61)
                    num = Shoulder_Reguration(num, theta1[0], 2.2, 0.06)
                elif(n == "3"):
                    theta1.append(-0.94)
                    num = Shoulder_Reguration(num, theta1[0], 2.5, 0.1)
                else:
                    print n
                """
                
                while(1):
                    x = g()
                    print x
                    if(str(x) == "1"):
                        m.setAngles(jointnames, pos.Rsearch_curtain, 0.05)
                        
                        print "4:left"
                        print "5:stop"
                        print "6:right"
                        print "0:next"
                        
                        while(1):
                            #キー入力
                            y = g()
                            
                            #NN使う場合↓
                            #shmemを介してpepperMain.cppにおけるNNのoutputを受け取る->yに
                            #y = DB.toPepper
                            
                            if(str(y) == "4"):
                                m.setAngles(jointnames[7], 0.0, 0.02)
                            elif(str(y) == "5"):
                                theta1 = m.getAngles(jointnames[7], False)
                                m.setAngles(jointnames[7], m.getAngles(jointnames[7], False), 0.5)
                                print "theta1:", theta1
                            elif(str(y) == "6"):
                                m.setAngles(jointnames[7], -1.0, 0.02)
                            elif(str(y) == "0"):
                                #theta1 = m.getAngles(jointnames[7], False)
                                #m.setAngles(jointnames[7], m.getAngles(jointnames[7], False), 0.5)
                                print "theta1:", theta1
                                m.setAngles([jointnames[8], jointnames[10]], [0.0, 0.6], 0.2)
                                time.sleep(2.0)
                                theta2 = m.getAngles(jointnames[10], False)
                                break
                            else:
                                print y
                        
                        #手首調節開始:11
                        time.sleep(1.0)
                        ws.Beep(1000, 300)
                        num = timer(num)
                        """
                        if(n == "1"):
                            num = Wrist_Reguration(num, 0.34, 2.0)
                            d = 26
                        elif(n == "2"):
                            num = Wrist_Reguration(num, 0.33, 2.0)
                            d = 27
                        elif(n == "3"):
                            num = Wrist_Reguration(num, 0.30, 2.0)
                            d = 30
                        else:
                            print n
                        """
                        """
                        m.setAngles(jointnames[10], 1.5, 0.02)
                        time.sleep(1.0)
                        theta2 = m.getAngles(jointnames[10], False)
                        m.setAngles(jointnames[10], theta2, 0.2)
                        print "theta2:", theta2
                                
                        #肘からペットボトルまでの距離
                        d = (5.0*math.cos(math.radians(theta2[0]*60))+4.0)/math.tan(math.radians(theta2[0]*60)) + 6.0
                        print "d:", d
                        """
                        print "8:up"
                        print "5:stop"
                        print "2:down"
                        print "0:next"
                        
                        while(1):
                            y = g()
                            if(str(y) == "2"):
                                m.setAngles(jointnames[10], 1.5, 0.01)
                            elif(str(y) == "5"):
                                theta2 = m.getAngles(jointnames[10], False)
                                m.setAngles(jointnames[10], theta2, 0.5)
                                print "theta2:", theta2
                                
                                #肘からペットボトルまでの距離
                                d = (5.0*math.cos(math.radians(theta2[0]*60))+4.0)/math.tan(math.radians(theta2[0]*60)) + 6.0
                                print "d:", d
                            elif(str(y) == "8"):
                                m.setAngles(jointnames[10], 0.0, 0.01)
                            elif(str(y) == "0"):
                                #m.setAngles(jointnames, pos.Rreaching1, 0.2)
                                break
                            else:
                                print y
                        
                        #つかむ準備姿勢:14
                        ws.Beep(1000, 300)
                        num = timer(num)
                        m.setAngles(jointnames, pos.Rsearch_curtain, 0.2)
                        time.sleep(2.0)
                        
                        r0 = 15   #回転軸から肩までの長さ
                        r1 = 18.1 #肩から肘までの長さ
                        r2 = 22   #肘から手のひらまでの長さ
                        
                        #ペットボトルの方向に回転:15
                        ws.Beep(1000, 300)
                        num = timer(num)
                        theta1[0] = math.radians(theta1[0]*60) - math.atan(5/(d+r1))
                        print math.radians(math.atan(5/(d+r1)))
                        print theta1[0]
                        m.moveTo(0.0, 0.0, theta1[0], 1.0)   #ペットボトルの方を向く
                        #m.setAngles(jointnames[7], theta1[0], 0.2)
                        
                        SH = math.sqrt(r1*r1 + r2*r2)    #最初の肩と手の距離
                        h = r2*(1 - 1/(math.sqrt(2)))    #ERを動かすときの振幅
                        s = r0*math.sin(-theta1[0])      
                        print "SH:", SH
                        print "h:", h
                        print "s:", s
                        
                        #距離が遠いと近づく:16
                        ws.Beep(1000, 300)
                        num = timer(num)
                        
                        d2 = 0
                        if(d+s+r1 > 40):
                            d2 = ((d+s+r1)-40)/100 + 0.03
                            print "d2:", d2
                            #.moveTo(d2*math.cos(theta1[0]), d2*math.sin(theta1[0]), 0.0)
                            m.moveTo(d2, 0.0, 0.0, 0.5)
                            position = l.getRobotPosition(True)
                            print "m.moveTo(d2, 0.0, 0.0, 0.5):", position
                            d = 40-s-r1
                            print "d:", d
                        
                        #手を伸ばす:17
                        ws.Beep(1000, 300)
                        num = timer(num)    
                        
                        theta3 = math.acos((r1*r1 + r2*r2 - (d+s+r1)*(d+s+r1))/(2*r1*r2)) #腕をd伸ばすのに必要な肘の角度
                        ERtheta = (180 - math.degrees(theta3))/60                     #ElbowpRollに入力する形に変換
                        theta4 = theta3 - Pi/2                                        #SholderPitchの計算に使う
                        print "theta3:", theta3
                        print "ERtheta:", ERtheta
                        print "theta4:", theta4
                    
                        theta5 = math.acos((r1*r1 + (d+s+r1)*(d+s+r1) - r2*r2)/(2*r1*(d+s+r1))) #手の高さを一定に保つのに必要な肩の角度
                        SPtheta = (math.degrees(theta5)-10)/60                            #SholderPitchに入力する形に変換
                        print "SPtheta:", SPtheta
                        #SRtheta = math.acos(math.cos(theta1[0])/math.cos(math.radians(SPtheta*60)))
                        #print "SRtheta:", SRtheta
                        
                        #手を伸ばす
                        m.setAngles([jointnames[6], jointnames[9], jointnames[10], jointnames[11]], [SPtheta, ERtheta, -0.5, 1.0], 0.2)
                        #m.setAngles([jointnames[6], jointnames[7], jointnames[9], jointnames[10], jointnames[11]], [SPtheta, SRtheta, ERtheta, -0.5, 1.0], 0.2)
                        
                        time.sleep(1.5)
                        #手を下ろす
                        SPtheta2 = SPtheta + 0.65
                        print "SPtheta2:", SPtheta2
                        #SRtheta2 = math.acos(math.cos(theta1[0])/math.cos(math.radians(SPtheta2*60)))
                        #print "SRtheta:", SRtheta
                        
                        m.setAngles(jointnames[6], SPtheta2, 0.05)
                        #m.setAngles(jointnames[6:8], [SPtheta2, SRtheta2], 0.05)
                        time.sleep(3.0)
                        
                        #持ち上げる
                        m.setAngles([jointnames[9], jointnames[10], jointnames[11]], [1.0, 1.0, 0.0], 0.05)
                        time.sleep(3.0)
                        m.setAngles([jointnames[6], jointnames[9]], [1.0, 1.5], 0.1)
                        time.sleep(2.0)
                        
                        position = l.getRobotPosition(True)
                        print "catch:", position
                        
                        #近づいた分戻って補正:18
                        ws.Beep(1000, 300)
                        num = timer(num)
                        
                        #m.moveTo(-d2*math.cos(theta1[0]), -d2*math.sin(theta1[0]), 0.0)
                        m.moveTo(-d2, 0.0, 0.0)
                    else:
                        break
                
                position = l.getRobotPosition(True)
                print "back after catch:", position
                #回転の補正
                m.moveTo(0.0, 0.0, (position1[2]-position[2])+math.radians(3.3))
                position = l.getRobotPosition(True)
                print position
                #併進移動の補正
                m.moveTo(position1[0]-position[0], position1[1]-position[1], 0.0)
                position = l.getRobotPosition(True)
                print (position)
                
                #後退:19
                ws.Beep(1000, 300)
                num = timer(num)
                
                m.moveTo(-position[0]-0.17, -position[1]+0.27, 0.0)
                
                position = l.getRobotPosition(True)
                print position
                
                for i in range(2):
                    homepos[i] = position[i]

                print "homepos:", homepos
                
                #補正:20
                ws.Beep(1000, 300)
                num = timer(num)
                
                m.moveTo(0.0, 0.0, -math.radians(7.25))
                time.sleep(1.0)
                #m.moveTo(0.0, 0.0, homepos[2]-position[2])
                
                position = l.getRobotPosition(True)
                print position
                
                #90度回転:21
                ws.Beep(1000, 300)
                num = timer(num)
                
                m.moveTo(0.0, 0.0, -Pi/2)
                
                #サイドテーブルへ移動:22
                ws.Beep(1000, 300)
                num = timer(num)
                
                m.moveTo(1.3, 0.1, 0.0, 4.0)
                time.sleep(1.0)
                
                #ペットボトルを置く:23
                ws.Beep(1000, 300)
                num = timer(num)
                
                #手を伸ばす
                m.setAngles([jointnames[6], jointnames[7], jointnames[9]], [55/60, 0.0,  40/60], 0.15)
                #m.setAngles(jointnames[7:12], putRArm, 0.2)
                time.sleep(2.0)
                #置く
                #m.setAngles([jointnames[6], jointnames[10], jointnames[11]], [30/60, -0.5, 1.0], 0.05)
                m.setAngles([jointnames[10], jointnames[11]], [-0.5, 1.0], 0.1)
                time.sleep(3.0)
                
                #手を挙げる:24
                ws.Beep(1000, 300)
                num = timer(num)
                
                m.setAngles(jointnames, pos.Rsearch_curtain, 0.15)
                time.sleep(2.0)
                
                #後退:25
                ws.Beep(1000, 300)
                num = timer(num)
                
                position = l.getRobotPosition(True)
                print position
                
                m.moveTo(-abs(homepos[1]-position[1]), -abs(homepos[0]-position[0]), 0.0)
                position = l.getRobotPosition(True)
                print position
                time.sleep(1.0)
                
                #回転:26
                ws.Beep(1000, 300)
                num = timer(num)
                
                m.moveTo(0.0, 0.0, homepos[2]-position[2])
                position = l.getRobotPosition(True)
                print position
                time.sleep(1.0)
                
                #位置補正:27
                ws.Beep(1000, 300)
                num = timer(num)
                
                m.moveTo(homepos[0]-position[0]-0.1, homepos[1]-position[1], 0.0)
                position = l.getRobotPosition(True)
                print position
                
                m.moveTo(0.0, 0.0, homepos[2]-position[2]-math.radians(3.3))
                position = l.getRobotPosition(True)
                print position
                #m.setAngles(jointnames, pos.b2, 0.2)
                
                p.goToPosture("StandInit", 0.3)
                
                time.sleep(2.0)
                
            elif(str(x) == "2"):
                #カーテンの開閉
                tts.say("カーテンですね")
                print ("curtain")
                time.sleep(2.0)
                
            elif(str(x) == "3"):
                #床に落ちたものを拾う
                tts.say("床ですね")
                print ("floor")
                time.sleep(2.0)
                
            #終了
            ws.Beep(1000, 300)
            time.sleep(1.0)
            ws.Beep(1000, 300)
            time.sleep(1.0)
            ws.Beep(1000, 700)
                
            #csvファイルへ書き込み
            now = datetime.datetime.now()
            filename = "log" + now.strftime("%Y%m%d%H%M%S") + ".csv"
            with open(filename, "w") as f:
                writer = csv.writer(f, lineterminator="\n")
                writer.writerow(commandlog)
                writer.writerow(timelog)
                writer.writerow(countlog)
                writer.writerow(freqlog)
        
        elif(str(x) == "2"):
                break

if __name__ == "__main__":
    main()
    
        
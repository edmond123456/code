# -*- coding: utf-8 -*-
"""
Created on 2018/05/14

@author: Junjie Hua
"""

from naoqi import ALProxy
import time
import datetime
import csv
import math
import getch
import postures as pos
import functions as func
import winsound as ws
import ctypes
import ctypes.wintypes
#import shmem

#akiyama 20170125
#import shmem

#DB = shmem.Shmem(True)
delay = 0.1

IP = "192.168.1.174"
PORT = 9559
localIP = "localhost"
localPORT = 64355
Pi = math.radians(180)


# 自律モードをOFFにする
awareness=ALProxy("ALBasicAwareness",ip_wifi,port_wifi)
awareness.stopAwareness()
autoMove=ALProxy("ALAutonomousMoves",ip_wifi,port_wifi)
autoMove.setBackgroundStrategy("none")
autoMove.setExpressiveListeningEnabled(0)

r0 = 0.15   #回転軸から肩までの長さ
r1 = 0.181 #肩から肘までの長さ
r2 = 0.22   #肘から手のひらまでの長さ

jointnames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand",
              "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand",
              "HeadPitch", "HeadYaw", "HipPitch", "HipRoll"]
"""
関節の番号の対応
jointnames = [0, 1, 2, 3, 4, 5
              6, 7, 8, 9, 10, 11
              12, 13, 14, 15]
"""


#akiyama 20170125
#C++mainconsoleを立ち上げてから
#DB = shmem.Shmem(True)
delay = 0.2
g = getch._Getch()

while(1):
    print("1:robot, 2:virtual robot")
    x = g()
        
    if(str(x) == "1"):
        m = ALProxy("ALMotion", IP, PORT)
        p = ALProxy("ALRobotPosture", IP, PORT)
        l = ALProxy("ALLocalization", IP, PORT)
        tts = ALProxy("ALTextToSpeech", IP, PORT)
        break
    elif(str(x) == "2"):
        m = ALProxy("ALMotion", localIP, localPORT)
        p = ALProxy("ALRobotPosture", localIP, localPORT)
        l = ALProxy("ALLocalization", localIP, localPORT)
        tts = ALProxy("ALTextToSpeech", localIP, localPORT)
        break
    else:
        print "no input", x
    


#この関数を起動するとペッパーの横レーザーが動き、ペッパーの手の中心から
#レーザーを止めた位置までの直線距離が求める。
#ペッパーからのx軸方向の距離を返す(xは縦方向である事に注意)。
def MeasureDistance(WristTheta, num):
    m.setAngles(jointnames, pos.b2, 0.2)
    time.sleep(0.5)
    m.setAngles([jointnames[8], jointnames[10]], [0.0, WristTheta], 0.2)
    print "Show command  2:laser down, 5:laser stop, 8:laser up, 0:Go"
    phi = 100
    while(1):
        x = g()
        
        #NN使う場合↓
        #shmemを介してpepperMain.cppにおけるNNのoutputを受け取る->yに
        #y = DB.toPepper
        #入力が変化した場合pepperに反映
        #idx = DB.toPepper
        #if(past_idx != idx):
        #    time.sleep(delay)
        #   y = idx + 4
        #    past_idx = idx
        
        if(str(x) == "2"):
            print "down"
            if(num == 1):   #numによって手首の回る速さが変わる
                m.setAngles(jointnames[10], 1.5, 0.02)
            elif(num == 2 or num == 3 or num == 4):
                m.setAngles(jointnames[10], 1.5, 0.01)

        elif(str(x) == "5"):
            print "stop"
            phi = m.getAngles(jointnames[10], False)[0]
            m.setAngles(jointnames[10], phi, 0.5)
            
            if(num == 1):    #スタート位置からカーテンの前までの距離を測る場合
                Distance = 0.9*math.tan(math.radians(90-phi*60))
                
            elif(num == 2):  #カーテンの前で掴む位置をまでの距離を測る場合
                Distance = (0.15+(0.07-0.07*math.cos(math.radians(abs(phi)*60))))/math.tan(math.radians(abs(phi)*60)) - 0.07*math.sin(math.radians(abs(phi)*60)) + 0.1
            
            elif(num == 3):  #ペットボトルまでの距離を測る場合
                Distance = (0.05*math.cos(math.radians(phi*60)) + 0.04)/math.tan(math.radians(phi*60)) + 0.05*math.sin(math.radians(phi*60)) #0.06
            
            elif(num == 4):
                Distance = (0.05*math.cos(math.radians(phi*60)) + 0.16)/math.tan(math.radians(phi*60)) + 0.05*math.sin(math.radians(phi*60)) #0.06
                
            print "phi:", phi
            print "Distance:", Distance

        elif(str(x) == "8"):
            print "Up"
            if(num == 1):   #numによって手首の回る速さが変わる
                m.setAngles(jointnames[10], -1.5, 0.02)
            elif(num == 2 or num == 3 or num == 4):
                m.setAngles(jointnames[10], -1.5, 0.01)

        elif(str(x) == "0"):    #出発する
            if(phi == 100): #phiが決定していない場合はループを抜けない
                print "phi is not desided."
                continue
            
            print "Go"
            tts.say("いってきますね")
            break

        else:
            print x, "no input"

    #握った手の中心からカーテンまでの距離を求めてる。
    #肘を曲げているので、ペッパーの動く中心からs(=0.21m)離れている事に注意。
    #DisToCurtain = (0.25+(0.07-0.07*math.cos(math.radians(abs(phi)*60))))/math.tan(math.radians(abs(phi)*60)) - 0.07*math.sin(math.radians(abs(phi)*60)) + 0.1
    #DisToCurtainに10cmの誤差修正を加えた
    print "phi:", phi
    print "Distance:", Distance
    return Distance
    
##################腕を伸ばすときに使う関数###############################
def ReachingPet(Dis):
    StoH = math.sqrt(r1*r1 + r2*r2)    #ERが90度の時の肩と手の距離
    print "StoH", StoH
    
    #手が届かない場合，手が届く距離まで近づく
    Dis3 = 0
    if(Dis+r1 > 0.4):
        Dis3 = ((Dis + r1) - 0.4) + 0.03
        print "Dis3:", Dis3
        m.moveTo(Dis3, 0.0, 0.0, 3.0)
        Dis = 0.4-r1
        print "Dis:", Dis
    
    elif(Dis+r1 < StoH):
        Dis3 = ((Dis + r1) - 0.4) - 0.03
        print "Dis3:", Dis3
        m.moveTo(-Dis3, 0.0, 0.0, 3.0)
        Dis = 0.4-r1
        print "Dis:", Dis
    
    #腕をDisToCurtain伸ばすのに必要なElboeRollの角度を計算
    theta4 = math.acos((r1*r1 + r2*r2 - (Dis + r1)*(Dis + r1))/(2*r1*r2))
    ERtheta = (180 - math.degrees(theta4))/60   #ElbowpRollに入力する形に変換
    print "ERtheta:", ERtheta    

    #手の高さを一定に保つのに必要なSholderPitchの角度を計算
    theta5 = math.acos((r1*r1 + (Dis + r1)*(Dis + r1) - r2*r2)/(2*r1*(Dis + r1)))
    SPtheta = (math.degrees(theta5)-10)/60      #SholderPitchに入力する形に変換
    print "SPtheta:", SPtheta
    
    return [SPtheta, ERtheta, Dis3]

#---------------------照準動作（キーボード入力）-----------------------
def Aiming(PosTheta, s, num, timelog, countlog, freqlog, 
           commandlog, keylog, keytimelog, positionlog):
    frag = 0
    
    m.setAngles(jointnames, pos.b2, 0.2)
    time.sleep(2.0)
    
    
    ws.Beep(1000, 300)
    num = func.logs(s, num, timelog, countlog, freqlog, commandlog)
    keylog.append("start")
    keytimelog.append(time.time()-s)
    
    print("command 0:OK, 2:down, 4:left, 5:stop, 6:right, 8:up")
    
    while(1):
        x = g() #デバッグ用
        """
        x = DB.toPepper
        time.sleep(delay)
        idx = DB.toPepper
        if(x != idx):   #一瞬だけ出力されるような間違ったコマンドを排除
            continue
        """
        if(str(x) == "2"): #右 5の次に入力すると停止　4の次に入力すると掴みに行く
            keylog.append(x)
            keytimelog.append(time.time()-s)
            num = func.logs(s, num, timelog, countlog, freqlog, commandlog)
            
            if(frag == 0 or frag == 2):
                print "right", x
                m.moveToward(0.0, 0.0, -0.1)
                frag = 2
            
            elif(frag == 5):
                print "stop", x
                m.moveToward(0.0, 0.0, 0.0)
                frag = 0
                
            elif(frag == 1):
                print "stop", x
                frag = 9
                
                    
        elif(str(x) == "5"): #左　２の次に入力すると停止
            keylog.append(x)
            keytimelog.append(time.time()-s)
            num = func.logs(s, num, timelog, countlog, freqlog, commandlog)
            
            if(frag == 0 or frag == 5):
                print "left", x
                m.moveToward(0.0, 0.0, 0.1)
                frag = 5
            
            elif(frag == 2):
                print "stop", x
                m.moveToward(0.0, 0.0, 0.0)
                frag = 0
            
            
        elif(str(x) == "3"): #上　４の次に入力すると停止
            keylog.append(x)
            keytimelog.append(time.time()-s)
            num = func.logs(s, num, timelog, countlog, freqlog, commandlog)
            
            if(frag == 1 or frag == 3):
                print "up", x
                m.setAngles(jointnames[10], -1.5, 0.01)
                frag = 3
            
            elif(frag == 4):
                print "stop", x
                phi = m.getAngles(jointnames[10], False)[0]
                m.setAngles(jointnames[10], phi, 0.5)
                Distance = (0.05*math.cos(math.radians(phi*60)) + 0.1)/math.tan(math.radians(phi*60)) + 0.05*math.sin(math.radians(phi*60)) + 0.06
                frag = 1
            
                    
        elif(str(x) == "4"): #下　３の次に入力すると停止　2or5の次に入力するとレーザーを横に
            keylog.append(x)
            keytimelog.append(time.time()-s)
            num = func.logs(s, num, timelog, countlog, freqlog, commandlog)
            
            if(frag == 1 or frag == 4):
                print "down", x
                m.setAngles(jointnames[10], 1.5, 0.01)
                frag = 4
            
            elif(frag == 3):
                print "stop", x
                phi = m.getAngles(jointnames[10], False)[0]
                m.setAngles(jointnames[10], phi, 0.5)
                Distance = (0.05*math.cos(math.radians(phi*60)) + 0.1)/math.tan(math.radians(phi*60)) + 0.05*math.sin(math.radians(phi*60)) + 0.06
                frag = 1
                
            elif(frag == 0):
                print "change", x
                m.setAngles([jointnames[8], jointnames[10]], [0.0, 1.0], 0.2)
                frag = 1
        
                
        else:
            if(frag == 9):
                break
            print "no input", x
        
      
    Theta = 0
    return [Theta, Distance]

#------------------------ドリンクを取る動作--------------------------------------
def drink(s, num, homepos, timelog, countlog, freqlog, commandlog, positionlog, keylog, keytimelog):
    #レーザーを床に撃つ:3
    #ws.Beep(1000, 300)
    #num = func.logs(s, num, timelog, countlog, freqlog, commandlog)
    #num = timer(num, timelog, countlog, freqlog, commandlog)
    
    """
    #進行方向調整
    theta0 = MeasureTheta(homepos[2])
    print "theta0:", theta0

    DisToTable = MeasureDistance(1.2, 1)
    print "DisToTable:", DisToTable
    """
    """
    #前進:4
    time.sleep(2.0)
    ws.Beep(1000, 300)
    num = func.logs(s, num, timelog, countlog, freqlog, commandlog)
    #num = timer(num, timelog, countlog, freqlog, commandlog)
    
    m.moveTo(1.4, 0.0, 0.0, 8.0)
    time.sleep(2.0)
    
    positionlog.append(l.getRobotPosition(True))
    #position = l.getRobotPosition(True)
    print "position:", positionlog
    """
    
    #肩調節の姿勢へ:6
    ws.Beep(1000, 300)
    num = func.logs(s, num, timelog, countlog, freqlog, commandlog)
    #num = timer(num, timelog, countlog, freqlog, commandlog)
    
    position = l.getRobotPosition(True)
    positionlog.append(l.getRobotPosition(True))
    #print "position2:", positionlog[2]
    
    #------------------肩調節----------------------------------
            
    ThetaDis = Aiming(position[2], s, num, timelog, countlog, freqlog, 
           commandlog, keylog, keytimelog, positionlog)    
    
    #------------手首調節開始:11----------------------
    time.sleep(1.0)
    ws.Beep(1000, 300)
    num = func.logs(s, num, timelog, countlog, freqlog, commandlog)
    #num = timer(num)
    
    #----------------つかむ準備姿勢:14-----------------------
    #ws.Beep(1000, 300)
    #num = func.logs(s, num, timelog, countlog, freqlog, commandlog)
    #num = timer(num)
    m.setAngles(jointnames, pos.Rsearch_curtain, 0.2)
    time.sleep(2.0)
    
    SPERDis = ReachingPet(ThetaDis[1])

    
    #手を伸ばす
    m.setAngles([jointnames[6], jointnames[9], jointnames[10], jointnames[11]], [SPERDis[0], SPERDis[1], -0.5, 1.0], 0.2)
    time.sleep(1.5)
    
    #手を下ろす
    SPtheta2 = SPERDis[0] + 0.65
    print "SPtheta2:", SPtheta2
    
    m.setAngles(jointnames[6], SPtheta2, 0.05)
    time.sleep(3.0)
    
    #持ち上げる
    m.setAngles([jointnames[9], jointnames[10], jointnames[11]], [1.0, 1.0, 0.0], 0.05)
    time.sleep(3.0)
    m.setAngles([jointnames[6], jointnames[9]], [1.0, 1.5], 0.1)
    time.sleep(1.0)
    
    #近づいた分戻って補正:18
    ws.Beep(1000, 300)
    num = func.logs(s, num, timelog, countlog, freqlog, commandlog)
    #num = timer(num)
    
    #m.moveTo(-d2*math.cos(theta1[0]), -d2*math.sin(theta1[0]), 0.0)
    m.moveTo(-SPERDis[2], 0.0, 0.0)
    
    m.moveTo(0.0, 0.0, -(l.getRobotPosition(True)[2] - homepos[2]))
    
    time.sleep(2.0)
    
    #回転の補正
    #m.moveTo(0.0, 0.0, -theta1)
    #m.moveTo(0.0, 0.0, (position1[2]-position[2])+math.radians(3.3))
    #position = l.getRobotPosition(True)
    #print position
    #併進移動の補正
    #m.moveTo(position1[0]-position[0], position1[1]-position[1], 0.0)
    #position = l.getRobotPosition(True)
    #print (position)
    
    #終了
    ws.Beep(1000, 300)
    time.sleep(1.0)
    ws.Beep(1000, 300)
    time.sleep(1.0)
    ws.Beep(1000, 700)
    num = func.logs(s, num, timelog, countlog, freqlog, commandlog)
        
    #csvファイルへ書き込み
    now = datetime.datetime.now()
    filename = "log" + now.strftime("%Y%m%d%H%M%S") + ".csv"
    with open(filename, "w") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(commandlog)
        writer.writerow(timelog)
        writer.writerow(countlog)
        writer.writerow(freqlog)
        writer.writerow(keylog)
        writer.writerow(keytimelog)
        
    del commandlog[1:]
    del timelog[1:]
    del countlog[1:]
    del freqlog[1:]
    del keylog[1:]
    del keytimelog[1:]

if __name__ == "__drink__":
    drink()    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
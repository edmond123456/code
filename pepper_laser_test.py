"""
created by Hua Junjie 2018/07/11
when keydown s pepper will move forward at the maximum velocity
when keyup s pepper will  stop
"""

from naoqi import ALProxy
import msvcrt
import sys
import time

localip = "localhost"
localport = 61690
#motion = ALProxy("ALMotion", localip, localport)
motion = ALProxy("ALMotion", "192.168.1.69", 9559)

MaxAccXY = 0.55
MaxVelXY = 0.55
t0 = time.clock()


num=0
while 1:
    c=msvcrt.getch()
    if c == 's':
        num=num+1
        if num%2==1:
            motion.moveToward(1.0, 0.0, 0.0,
                          [["MaxVelXY", MaxVelXY], ["MaxAccXY", MaxAccXY]])
            #time.sleep(0.05)
        else:
            motion.moveToward(0.0, 0.0, 0.0,
                          [["MaxVelXY", MaxVelXY], ["MaxAccXY", MaxAccXY]])
    #if time.clock()-t0>=10:
    #    print "10s"
    #    motion.stopMove()
    #    break







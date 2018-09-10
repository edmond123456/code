# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 13:20:26 2018

@author: Hua
"""

import sys
print "\n".join(sys.path)


from naoqi import ALProxy
#tts = ALProxy("ALTextToSpeech", "192.168.1.109", 9559)
motion = ALProxy("ALMotion", "192.168.1.69", 9559)
tts = ALProxy("ALTextToSpeech", "192.168.1.69", 9559)
motion.wakeUp()
tts.say("こんにちは、私はpepperです。")





"""
Created on 2018/07/11
stop all behavior

@author: Hua
"""
#import sys
#print "\n".join(sys.path)
#from naoqi import ALProxy
#behavior = ALProxy("ALBehaviorManager", "192.168.1.69", 9559)
#behavior.stopAllBehaviors()



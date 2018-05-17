#! /usr/bin/python
# it requires "chmod +x mypythonscript.py" to be called by ROS

import rospy
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image
from std_msgs.msg import Bool
from std_msgs.msg import String
from std_msgs.msg import Float32
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import time
import math
from numpy import *
import os.path
import tt2_pack.Classification as Classification

#Constants
path_user=rospy.get_param('path_user')
path_classifier=rospy.get_param('Clasificador')


def image_callback(ros_data):
    global state_current
    global state_prev, recognition
    state_current=ros_data.data
    if state_current^state_prev:
        if state_current:
            #print 'Imges Completed'
            nameAvrg=Classification.user_recognized(path_user,path_classifier)
            name=nameAvrg[0]
            print 'Welcome Sir '+name
            if name != 'NO USER IN THE DATA BASE':
                userDet= 'Hola ' + name
                average.publish(nameAvrg[1])
                recognition.publish(userDet)                
                publica.publish(True)
            else:
                recognition.publish('Usuario No Registrado')
                average.publish(nameAvrg[1])
                publica.publish(False)

        else:
            print 'No user detected'
            publica.publish(False)
            recognition.publish('Coloquese Dentro del Recuadro')
            
    state_prev=ros_data.data

def main():
    global state_current
    global state_prev
    global publica, recognition
    global average
    state_prev=True
    state_current=False
    rospy.init_node('recognition_node')
    image_topic = '/user_images'
    rospy.Subscriber(image_topic, Bool, image_callback,queue_size=1)
    recognition = rospy.Publisher('/user_name', String, queue_size=10)
    publica = rospy.Publisher('User_detection',Bool,queue_size=1)
    average = rospy.Publisher('/average',Float32,queue_size=1)
   
    rospy.spin()

if __name__ == '__main__':
    main()
#! /usr/bin/python
# it requires "chmod +x mypythonscript.py" to be called by ROS

import rospy
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import time
import math
from numpy import *

#Constants
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
bridge = CvBridge()
    
def image_callback(ros_data):
    try:
        np_arr = np.fromstring(ros_data.data, np.uint8)
        cv2_img = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)

    except CvBridgeError, e:
        print(e)
    else:
        e1 = cv2.getTickCount()
        image1 = np.asarray(cv2_img) # 480x640x3
        gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            #cv2.rectangle(image1,(x,y),(x+w,y+w+25),(255,0,0),1)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = image1[y:y+h, x:x+w]
        imageF=image1[y:y+w+20, x:x+w]
        imF=cv2.resize(imageF,(150,150))

    # Compress image to pub ------------------------------------------------
        cropImage = CompressedImage()
        cropImage.header.stamp = rospy.Time.now()
        cropImage.format = "jpeg"
        cropImage.data = np.array(cv2.imencode('.jpg',imF)[1]).tostring()
        pub.publish(cropImage)

    # Print stats ----------------------------------------------------------
        e2 = cv2.getTickCount() 
        t = (e2 - e1)/cv2.getTickFrequency()    
    
    print('frame time:'+str(t)+'-------------------------------block end')

def main():

    global pub

    rospy.init_node('im_prepros_c')
    image_topic = "/im_prepros/compressed"
    rospy.Subscriber(image_topic, CompressedImage, image_callback,queue_size=1)
    pub = rospy.Publisher('/im_prepros_AI/compressed', CompressedImage, queue_size=1)

    rospy.spin()

if __name__ == '__main__':
    main()
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

bridge = CvBridge()

def apagar():
	print "Base de datos completa!"	

def image_callback(ros_data):

    try:
    # Convert your ROS Image message to OpenCV2

	np_arr = np.fromstring(ros_data.data, np.uint8)
	cv2_img = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)

    except CvBridgeError, e:
        print(e)

    else:
	# Image pre-processing function begins
	global count
	global count2
	e1 = cv2.getTickCount()

	# 1. Convert data received to numpy array
	image = np.asarray(cv2_img) # 3 Canales
	# 2. Color transform ---------------------------------------------
	color = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# 3. Histogram Calculation ---------------------------------------
	clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(18,18))
	cl1 = clahe.apply(color)
	equ = cv2.equalizeHist(color)
	#Union of the 3 images
	dst=np.hstack((color,equ,cl1))

	# Compress image to pub ------------------------------------------------
        cropImage = CompressedImage()
        cropImage.header.stamp = rospy.Time.now()
        cropImage.format = "jpeg"
        cropImage.data = np.array(cv2.imencode('.jpg',dst)[1]).tostring()
        pub.publish(cropImage)

	# Print stats ----------------------------------------------------------
	e2 = cv2.getTickCount()	
    	t = (e2 - e1)/cv2.getTickFrequency()
    	#print('frame time:'+str(t)+'----------------------------block end')
	
	count+=1
	if count==25:
		count2+=1
		count=0
		print('Frame :'+str(count2)+'----------------------------block end')
		#cv2.imwrite("dataBase/s10/%d.jpg" % count2, color)     # save frame as JPEG file
		if count2==10:
			rospy.on_shutdown(apagar)


        

def main():

    global pub
    global count
    global count2
    count2=0
    count=0
    rospy.init_node('im_prepros_c')
    image_topic = "/im_prepros_AI/compressed"
    rospy.Subscriber(image_topic, CompressedImage, image_callback,queue_size=1)
    pub = rospy.Publisher('/im_prepros_eq/compressed', CompressedImage, queue_size=1)
    
    rospy.spin()

if __name__ == '__main__':
    main()


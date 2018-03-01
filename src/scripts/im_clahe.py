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
import os.path

#Constants

face_cascade = cv2.CascadeClassifier(rospy.get_param('haar'))
bridge = CvBridge()
    
def image_callback(ros_data):

    try:
        np_arr = np.fromstring(ros_data.data, np.uint8)
        cv2_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    except CvBridgeError, e:
        print(e)
    else:

        image1 = np.asarray(cv2_img) # 480x640x3
        cv2.rectangle(image1,(220,140),(420,340),(0,0,255),4)
        image = image1[140:340,220:420]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        e1 = cv2.getTickCount()
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
        try:
            pass
            imF=cv2.resize(roi_gray,(150,150))
            e2 = cv2.getTickCount()
            t = (e2 - e1)/cv2.getTickFrequency()
            # Image pre-processing function begins
            # 3. Histogram Calculation ---------------------------------------
            clahe = cv2.createCLAHE(clipLimit=5, tileGridSize=(8,8))
            cl1 = clahe.apply(imF)
            # Print stats ----------------------------------------------------------
            print('frame time:'+str(t)+'-------------------------------block end')
            # Compress image to pub ------------------------------------------------
            cropImage = CompressedImage()
            cropImage.header.stamp = rospy.Time.now()
            cropImage.format = "jpeg"
            cropImage.data = np.array(cv2.imencode('.jpg',cl1)[1]).tostring()
            pub.publish(cropImage)

        except UnboundLocalError:
            print 'NO HAY ROSTRO EN LA IMAGEN', len(faces)
            #pub.publish(None)
        finally:
            #Crear compressed image de la imagen con el recuadro
            img_rec = CompressedImage()
            img_rec.header.stamp = rospy.Time.now()
            img_rec.format = "jpeg"
            img_rec.data = np.array(cv2.imencode('.jpg',image1)[1]).tostring()
            pub2.publish(img_rec)



def main():
    global pub
    global pub2
    rospy.init_node('im_prepros_c')
    image_topic = "/im_prepros/compressed"
    image_topic_camera='/usb_cam/image_raw/compressed'
    rospy.Subscriber(image_topic_camera, CompressedImage, image_callback,queue_size=1)
    pub = rospy.Publisher('/Clahe/compressed', CompressedImage, queue_size=1)
    pub2 = rospy.Publisher('/Recuadro/compressed', CompressedImage, queue_size=1)

    rospy.spin()

if __name__ == '__main__':
    main()

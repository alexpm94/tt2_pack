#! /usr/bin/python
# it requires "chmod +x mypythonscript.py" to be called by ROS

import rospy
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image
from std_msgs.msg import Bool
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import time
import math
from numpy import *
import os.path

#Constants

face_cascade = cv2.CascadeClassifier(rospy.get_param('haar'))
path_user=rospy.get_param('path_user')
bridge = CvBridge()

def user_images(path,cont,image):
    cv2.imwrite((path+"/%d.png") % cont, image)

def create_CI(image):
	'''
	This function creates a Compressed image object and it sets
	its parameters, it needs as argument the name of the image.
	'''
	msg = CompressedImage()
	msg.header.stamp = rospy.Time.now()
	msg.format = "jpeg"
	msg.data = np.array(cv2.imencode('.jpg',image)[1]).tostring()
	return msg
    
def image_callback(ros_data):
    global contador
    try:
        np_arr = np.fromstring(ros_data.data, np.uint8)
        cv2_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    except CvBridgeError, e:
        print(e)
    else:#La linea else se ejecuta cuanto no hay exceptions

        image1 = np.asarray(cv2_img) # 480x640x3
        cv2.rectangle(image1,(180,100),(480,380),(0,0,255),4)
        image = image1[100:380,180:480]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        e1 = cv2.getTickCount()
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h+5, x+5:x+w-10]
        try:
            pass
            imF=cv2.resize(roi_gray,(140,160))
            e2 = cv2.getTickCount()
            t = (e2 - e1)/cv2.getTickFrequency()
            # Image pre-processing function begins
            # 3. Histogram Calculation ---------------------------------------
            clahe = cv2.createCLAHE(clipLimit=5, tileGridSize=(8,8))
            cl1 = clahe.apply(imF)
            # Print stats ----------------------------------------------------------
            #print('frame time:'+str(t)+'-------------------------------block end')
            faces_str='ROSTRO DTECTADO'
            if contador<10:
                user_images(path_user,contador,cl1)
            elif contador==11:
                pub4.publish(True)
            contador+=1
            # Compress image to pub ------------------------------------------------
            cropImage = create_CI(cl1)
            pub.publish(cropImage)
            pub3.publish(faces_str)

        except UnboundLocalError:
            faces_str='NO HAY ROSTRO'
            contador=0
            pub3.publish(faces_str)
            pub4.publish(False)

        finally:
            #Crear compressed image de la imagen con el recuadro
            img_rec = create_CI(image1)
            pub2.publish(img_rec)



def main():
    global pub
    global pub2
    global pub3
    global pub4
    global contador
    contador=0
    rospy.init_node('im_prepros_c')
    image_topic = "/im_prepros/compressed"
    image_topic_camera='/usb_cam/image_raw/compressed'
    rospy.Subscriber(image_topic_camera, CompressedImage, image_callback,queue_size=1)
    pub = rospy.Publisher('/Clahe/compressed', CompressedImage, queue_size=1)
    pub2 = rospy.Publisher('/Recuadro/compressed', CompressedImage, queue_size=1)
    pub3 = rospy.Publisher('faces_founded', String, queue_size=10)
    pub4 = rospy.Publisher('user_images', Bool, queue_size=1)

    rospy.spin()

if __name__ == '__main__':
    main()

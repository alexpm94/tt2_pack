#! /usr/bin/python
# it requires "chmod +x mypythonscript.py" to be called by ROS

import rospy
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image as ImageMsg
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import time
import math
import os.path
from Tkinter import *
from PIL import Image, ImageTk

#Constants


bridge = CvBridge()


    
    
    
def image_callback(data):   
     
        #Prara usar Bolsas
        #np_arr = np.fromstring(ros_data.data, np.uint8)
        #cv2_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        #Para usar imagenes de camara
    
    cv2_img = bridge.imgmsg_to_cv2(data, "bgr8")
    image1 = np.asarray(cv2_img) # 480x640x3
    cv2image = cv2.cvtColor(image1, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.image=imgtk
        
  

def listener():
    global lmain
    rospy.init_node('im_prepros_c',anonymous=True)
    image_topic = "/usb_cam/image_raw/"
    rospy.Subscriber(image_topic, ImageMsg, image_callback,queue_size=1)
     # spin() simply keeps python from exiting until this node is stopped
    root = Tk()
    root.bind('<Escape>', lambda e: root.quit())
    frame1=Frame(root)
    frame1.pack()
    lmain = Label(frame1)
    lmain.pack()
    quitButton=Button(root, text="Quit", command=root.quit)
    quitButton.pack()
    mainloop()

if __name__ == '__main__':
    global lmain
    global imgtk
   

    listener()
    

    
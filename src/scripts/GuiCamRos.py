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
from std_msgs.msg import String
import roslaunch

#Constants
bridge = CvBridge()    
    
def image_callback(data):   
    global lmain
        #Prara usar Bolsas
    np_arr = np.fromstring(data.data, np.uint8)
    cv2_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        #Para usar imagenes de camara    
    #cv2_img = bridge.imgmsg_to_cv2(data, "bgr8")
    image1 = np.asarray(cv2_img) # 480x640x3
    cv2image = cv2.cvtColor(image1, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.image=imgtk
        
def label_callback(data):
    global lfaces    
    lfaces.configure(text=data.data)

def quit():
    global root
    global launch
    launch.shutdown()
    root.quit()
 

def main():
    global lmain
    global lfaces
    global root

    rospy.init_node('im_prepros_c',anonymous=True)
    
    image_topic = "/Recuadro/compressed"
    rospy.Subscriber(image_topic, CompressedImage, image_callback,queue_size=1)
    faces_topic = "/faces_founded"
    rospy.Subscriber(faces_topic, String, label_callback,queue_size=1)
     # spin() simply keeps python from exiting until this node is stopped
    root = Tk()
    #root.attributes("-fullscreen", True)
    #Specific Size
    #root.geometry("720x500")
    #Full view Size
    #root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    #root.bind('<Escape>', lambda e: root.attributes("-fullscreen", True))
    frame1=Frame(root)
    frame1.pack(side=RIGHT)
    lmain = Label(frame1)
    lmain.pack(side=TOP)
    lfaces=Label(frame1)
    lfaces.pack(side = BOTTOM)
    root.bind('<Escape>', lambda e: root.quit())
    quitButton=Button(root, text="Quit", command=quit)
    quitButton.pack(side = BOTTOM)
    mainloop()

def launch():
    global launch
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/dany/catkin_ws/src/tt2_pack/src/scripts/detection.launch"])

    launch.start()
    main()

if __name__ == '__main__':    
    launch()

    
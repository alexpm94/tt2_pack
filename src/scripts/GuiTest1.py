#! /usr/bin/env python
#
# GUI module generated by PAGE version 4.12
# In conjunction with Tcl version 8.6
#    Apr 09, 2018 05:57:48 PM

import sys
import rospy
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Bool
from sensor_msgs.msg import Image as ImageMsg
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import time
import math
import os.path
from PIL import Image as ImageZ, ImageTk
from std_msgs.msg import String
import roslaunch
import os
from time import sleep

launch_path= os.path.dirname(os.path.realpath(__file__))
try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import GuiTest_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global root, top, counter
    counter=0
    root = Tk()
    top = SEGURIFACE (root)
    GuiTest_support.init(root, top)
    root.mainloop()


def launch():
    global launch
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launch = roslaunch.parent.ROSLaunchParent(uuid, [launch_path+"/detection.launch"])

    launch.start()
    rospy.init_node('gui',anonymous=True)
    
    image_topic = "/Recuadro/compressed"
    rospy.Subscriber(image_topic, CompressedImage, image_callback,queue_size=1)
    faces_topic = "/faces_founded"
    rospy.Subscriber(faces_topic, String, label_callback,queue_size=1)
    

def image_callback(data):   
    global top
    #Prara usar Bolsas
    np_arr = np.fromstring(data.data, np.uint8)
    cv2_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        #Para usar imagenes de camara    
    #cv2_img = bridge.imgmsg_to_cv2(data, "bgr8")
    image1 = np.asarray(cv2_img) # 480x640x3
    cv2image = cv2.cvtColor(image1, cv2.COLOR_BGR2RGBA)
    cv2imflip = cv2.flip(cv2image, 1)
    cv2imresize = cv2.resize(cv2imflip, (732, 549)) 
    img = ImageZ.fromarray(cv2imresize)
    imgtk = ImageTk.PhotoImage(image=img)
    top.lImage.imgtk = imgtk
    top.lImage.configure(image=imgtk)
    top.lImage.image=imgtk

def image_callbackTuto(data):   
    global top
        #Prara usar Bolsas
    np_arr = np.fromstring(data.data, np.uint8)
    cv2_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        #Para usar imagenes de camara    
    #cv2_img = bridge.imgmsg_to_cv2(data, "bgr8")
    image1 = np.asarray(cv2_img) # 480x640x3
    cv2image = cv2.cvtColor(image1, cv2.COLOR_BGR2RGBA)
    cv2imflip = cv2.flip(cv2image, 1)
    cv2imresize = cv2.resize(cv2imflip, (230, 230)) 
    img = ImageZ.fromarray(cv2imresize)
    imgtk = ImageTk.PhotoImage(image=img)
    top.ImageTut.imgtk = imgtk
    top.ImageTut.configure(image=imgtk)
    top.ImageTut.image=imgtk
        
def label_callback(data):
    global top    
    top.Message.configure(text=data.data)

def quit():
    global root
    global launch
    try:
        launch.shutdown()
    except: pass
    finally:
        root.quit()

class MyDialog:
    def __init__(self, parent):
        self.top = Toplevel(parent)
        self.myLabel = Label(self.top, text='Escribe el nombre del nuevo ususario')
        self.myLabel.pack()

        self.myEntryBox = Entry(self.top)
        self.myEntryBox.pack()

        self.mySubmitButton = Button(self.top, text='Crear Usuario', command=self.send)
        self.mySubmitButton.pack()

    def send(self):
        self.username = self.myEntryBox.get()
        self.top.destroy()

    def getUser(self):
        return self.username

def my_callback(event):
    global counter, launch2,t1
    counter+=1
    if counter>10:
        launch2.shutdown()
        #Stop Timer, it doesnt work to kill the node
        t1.shutdown()
        counter=0
    print 'Counter: '+str(counter)

def complete_callback(rosdata):
    global launch2
    state=rosdata.data
    if state==True:
        launch2.shutdown()

def Save():
    global launch2,counter,t1
    inputDialog = MyDialog(root)
    root.wait_window(inputDialog.top)
    #Create User
    os.environ['User_name']=inputDialog.getUser()
    launch_path= os.path.dirname(os.path.realpath(__file__))
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launch2 = roslaunch.parent.ROSLaunchParent(uuid, [launch_path+'/record.launch'])
    launch2.start()
    rospy.init_node('Add_User',disable_signals=True,anonymous=True)
    #Show image in the frame
    image_topic = "/Recuadro/compressed"
    rospy.Subscriber(image_topic, CompressedImage, image_callback,queue_size=1)
    rospy.Subscriber("user_images",Bool,complete_callback)
    #Create timer object
    #t1=rospy.Timer(rospy.Duration(1), my_callback)

def toggle_fullscreen(self, event=None):
        root.state = not root.state  # Just toggling the boolean
        root.attributes("-fullscreen", root.state)
        return "break"

def end_fullscreen(self, event=None):
        root.state = False
        root.attributes("-fullscreen", False)
        return "break"      

class SEGURIFACE:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 

        top.geometry("1024x600+195+67")
        top.title("SEGURIFACE")
        top.configure(highlightcolor="black")
        top.bind("<F>", toggle_fullscreen)
        top.bind("<Escape>", end_fullscreen)


        self.Frame1 = Frame(top)
        self.Frame1.place(relx=0.0, rely=0.0, relheight=1.01, relwidth=0.29)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#296c5e")
        self.Frame1.configure(width=295)

        self.AddUser = Button(self.Frame1)
        self.AddUser.place(relx=0.03, rely=0.02, height=26, width=123)
        self.AddUser.configure(activebackground="#d9d9d9")
        self.AddUser.configure(text='''Agregar Usuario''')
        self.AddUser.configure(command=Save)

        self.Train = Button(self.Frame1)
        self.Train.place(relx=0.03, rely=0.08, height=26, width=79)
        self.Train.configure(activebackground="#d9d9d9")
        self.Train.configure(text='''Entrenar''')

        self.RecognizerB = Button(self.Frame1)
        self.RecognizerB.place(relx=0.03, rely=0.15, height=26, width=89)
        self.RecognizerB.configure(activebackground="#d9d9d9")
        self.RecognizerB.configure(text='''Reconocer''')
        self.RecognizerB.configure(command=launch)

        self.Quit = Button(self.Frame1)
        self.Quit.place(relx=0.3, rely=0.89, height=26, width=52)
        self.Quit.configure(activebackground="#d9d9d9")
        self.Quit.configure(text='''Salir''')
        self.Quit.configure(command=quit)

        self.ImageTut = Label(self.Frame1)
        self.ImageTut.place(relx=0.1, rely=0.45, height=230, width=230)
        self.ImageTut.configure(background="#0029ff")
        self.ImageTut.configure(width=296)

        self.Frame2 = Frame(top)
        self.Frame2.place(relx=0.29, rely=0.0, relheight=0.92, relwidth=0.71)
        self.Frame2.configure(relief=GROOVE)
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief=GROOVE)
        self.Frame2.configure(background="#00d9d9")
        self.Frame2.configure(width=730)

        self.lImage = Label(self.Frame2)
        self.lImage.place(relx=0.0, rely=0.0, height=549, width=732)
        self.lImage.configure(activebackground="#f9f9f9")
        

        self.Message = Label(top)
        self.Message.place(relx=0.53, rely=0.95, height=18, width=144)
        self.Message.configure(activebackground="#f9f9f9")

    
if __name__ == '__main__':
    vp_start_gui()

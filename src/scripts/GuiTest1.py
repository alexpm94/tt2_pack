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
import tt2_pack.readCSV as readCSV
import tt2_pack.recognitionTT2 as recognition
import cv2
import numpy as np
import time
import math
import os.path
from PIL import Image as ImageZ, ImageTk
from std_msgs.msg import String
import roslaunch
import os
import rospkg 

rospack = rospkg.RosPack()
Image_back=rospack.get_path('tt2_pack')+'/include/FondoFacialDetection.png'

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
    rospy.init_node('gui',anonymous=True)
    root = Tk()
    top = SEGURIFACE (root)
    GuiTest_support.init(root, top)
    root.mainloop()


def launch():
    global top 
    global launch
    global sub1,sub2
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launch = roslaunch.parent.ROSLaunchParent(uuid, [launch_path+"/detection.launch"])

    #top.ImageTut.place(relx=0.14, rely=0.42, height=240, width=220)
    top.lImage.place(relx=0.28, rely=-0.01, height=549, width=732)
    top.Message.place(relx=0.48, rely=0.08, height=23, width=300)

    launch.start()
    image_topic = "/Recuadro/compressed"
    sub1=rospy.Subscriber(image_topic, CompressedImage, image_callback,queue_size=1)
    faces_topic = "/user_name"
    sub2=rospy.Subscriber(faces_topic, String, label_callback,queue_size=1)
    

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
    cv2imresize = cv2.resize(cv2imflip, (240, 224)) 
    img = ImageZ.fromarray(cv2imresize)
    imgtk = ImageTk.PhotoImage(image=img)
    top.ImageTut.imgtk = imgtk
    top.ImageTut.configure(image=imgtk)
    top.ImageTut.image=imgtk
        
def label_callback(data):
    global top    
    top.Message.configure(text=data.data)

def stop():
    global launch, top, launch2, sub1, sub2
    try:
        launch.shutdown()
        sub1.unregister()
        sub2.unregister()
        launch2.shutdown()
    except:pass
    finally:
        top.lImage.place_forget()
        top.ImageTut.place_forget()
        top.Message.place_forget()


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
    global launch2, top, sub3, sub4, sub5
    state=rosdata.data
    if state==True:
        top.lImage.place_forget()
        top.ImageTut.place_forget()
        top.Message.place_forget()
        launch2.shutdown()
        sub3.unregister()
        sub4.unregister()
        sub5.unregister()
        #t1.signal_shutdown('Done') 

def Save():
    global launch2,counter,t1, sub3, sub4, sub5
    inputDialog = MyDialog(root)
    root.wait_window(inputDialog.top)
    top.lImage.place(relx=0.28, rely=-0.01, height=549, width=732)
    top.ImageTut.place(relx=0.025, rely=0.42, height=224, width=240)
    #Create User
    os.environ['User_name']=inputDialog.getUser()
    launch_path= os.path.dirname(os.path.realpath(__file__))
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launch2 = roslaunch.parent.ROSLaunchParent(uuid, [launch_path+'/record.launch'])
    launch2.start()
    #rospy.init_node('Add_User',disable_signals=True,anonymous=True)
    #Show image in the frame
    image_topic = "/Recuadro/compressed"
    sub3=rospy.Subscriber(image_topic, CompressedImage, image_callback,queue_size=1)
    sub4=rospy.Subscriber("user_images",Bool,complete_callback)
    sub5=rospy.Subscriber("/tuto/compressed", CompressedImage,image_callbackTuto, queue_size=1)
    #Create timer object
    #t1=rospy.Timer(rospy.Duration(1), my_callback)

def entrenar():
    readCSV.readCSV()
    recognition.recognition()

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
        font11 = "-family Ubuntu -size 15 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"
        font12 = "-family Ubuntu -size 13 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"

        top.geometry("1024x600+382+93")
        top.title("SEGURIFACE")
        top.configure(highlightcolor="black")
        top.bind("<F>", toggle_fullscreen)
        top.bind("<Escape>", end_fullscreen)

                   
        self.Frame1 = Frame(top)
        self.Frame1.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="1")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#296c5e")
        self.Frame1.configure(width=1024)

        self.Status = Label(self.Frame1)
        self.Status.place(relx=0.0, rely=0.0, height=600, width=1024)
        #self._img1 = PhotoImage(file="../../include/Fondo.png")
        self._img1 = PhotoImage(file=Image_back)
        self.Status.configure(image=self._img1)
        self.Status.configure(justify=LEFT)
        self.Status.configure(text='''Label''')
        self.Status.configure(width=1024)
        self.Status.configure(height=600)

        self.AddUser = Button(self.Frame1)
        self.AddUser.place(relx=0.07, rely=0.05, height=26, width=140)
        self.AddUser.configure(activebackground="#d9d9d9")
        self.AddUser.configure(background="#007090")
        self.AddUser.configure(borderwidth="0")
        self.AddUser.configure(font=font12)
        self.AddUser.configure(foreground="#ffffff")
        self.AddUser.configure(highlightthickness="0")
        self.AddUser.configure(text='''Agregar Usuario''')
        self.AddUser.configure(command=Save)

        self.Train = Button(self.Frame1)
        self.Train.place(relx=0.1, rely=0.14, height=26, width=80)
        self.Train.configure(activebackground="#d9d9d9")
        self.Train.configure(background="#007090")
        self.Train.configure(borderwidth="0")
        self.Train.configure(font=font12)
        self.Train.configure(foreground="#ffffff")
        self.Train.configure(highlightthickness="0")
        self.Train.configure(text='''Entrenar''')
        self.Train.configure(command=entrenar)

        self.RecognizerB = Button(self.Frame1)
        self.RecognizerB.place(relx=0.1, rely=0.22, height=26, width=90)
        self.RecognizerB.configure(activebackground="#d9d9d9")
        self.RecognizerB.configure(background="#007090")
        self.RecognizerB.configure(borderwidth="0")
        self.RecognizerB.configure(font=font12)
        self.RecognizerB.configure(foreground="#ffffff")
        self.RecognizerB.configure(highlightthickness="0")
        self.RecognizerB.configure(text='''Reconocer''')
        self.RecognizerB.configure(command=launch)

        self.StopLaunch = Button(self.Frame1)
        self.StopLaunch.place(relx=0.105, rely=0.3, height=26, width=74)
        self.StopLaunch.configure(activebackground="#d9d9d9")
        self.StopLaunch.configure(background="#007090")
        self.StopLaunch.configure(borderwidth="0")
        self.StopLaunch.configure(compound="center")
        self.StopLaunch.configure(font=font12)
        self.StopLaunch.configure(foreground="#ffffff")
        self.StopLaunch.configure(highlightthickness="0")
        self.StopLaunch.configure(text='''Detener''')
        self.StopLaunch.configure(command=stop)

        self.ImageTut = Label(self.Frame1)
        self.ImageTut.place(relx=0.01, rely=0.42, height=224, width=240)
        self.ImageTut.configure(activebackground="#f9f9f9")
        self.ImageTut.configure(background="#ffffff")
        self.ImageTut.configure(disabledforeground="#ffffff")
        #self._img2 = PhotoImage(file="../../include/upiita-logo.png")
        #self.ImageTut.configure(image=self._img2)
        self.ImageTut.configure(state=ACTIVE)
        self.ImageTut.configure(takefocus="1")
        self.ImageTut.configure(width=240)
        self.ImageTut.place_forget()  

        self.Quit = Button(self.Frame1)
        self.Quit.place(relx=0.11, rely=0.87, height=33, width=66)
        self.Quit.configure(activebackground="#d9d9d9")
        self.Quit.configure(background="#d10000")
        self.Quit.configure(compound="center")
        self.Quit.configure(font=font11)
        self.Quit.configure(foreground="#ffffff")
        self.Quit.configure(highlightbackground="#0000d9")
        self.Quit.configure(highlightthickness="0")
        self.Quit.configure(text='''Salir''')
        self.Quit.configure(command=quit)

        self.lImage = Label(self.Frame1)
        self.lImage.place(relx=0.28, rely=-0.01, height=549, width=732)
        self.lImage.configure(activebackground="#f9f9f9")
        self.lImage.place_forget()

        self.Message = Label(self.Frame1)
        self.Message.place(relx=0.57, rely=0.25, height=30, width=200)
        self.Message.configure(font=font11)
        self.Message.configure(activebackground="#f9f9f9")
        self.Message.place_forget()
    
if __name__ == '__main__':
    vp_start_gui()

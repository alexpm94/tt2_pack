#! /usr/bin/python
# it requires "chmod +x mypythonscript.py" to be called by ROS

import rospy
from std_msgs.msg import Bool


def user_callback(ros_data): #User_detected
	global blink_state
	global user_state

	estado=ros_data.data

	if estado:
		user_state=True
	if blink_state == False:
		user_state=False


def blink_callback(ros_data):	#Blink_detected
	global blink_state
	global pub_arduino
	global user_state

	state_current=ros_data.data

	if state_current:
		#print 'Blink_detected'
		blink_state=True
 	else:
		#print 'No blink detected'
		blink_state=False


	if user_state and blink_state:
		pub_arduino.publish(True)
		ardu=True
	else:
		pub_arduino.publish(False)
		ardu=False

	print ('blink state','user_state','Arduino')
	print ('',blink_state,'    ', user_state,'  ', ardu)


def main():

	global pub_arduino
 	global blink_state
 	global user_state
	global state_prev
	global state_current

	blink_state=False
	user_state=False
	state_prev=True
	state_current=False
	
	rospy.init_node('genuino_node')
	rospy.Subscriber('/User_detection', Bool, user_callback,queue_size=1)
	rospy.Subscriber('/Blink_detection', Bool, blink_callback,queue_size=1)

	pub_arduino = rospy.Publisher('genuinoState', Bool, queue_size=1)

    #blink_detected
	rospy.spin()

if __name__ == '__main__':

    main()



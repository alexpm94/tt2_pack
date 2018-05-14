#!/usr/bin/env python

import sys
import os.path
import csv
import rospkg 

def readCSV():
	rospack = rospkg.RosPack()
	# get the file path for rospy_tutorials
	CSV_Users=rospack.get_path('tt2_pack')+'/include/users.csv'
	CSV_Images=rospack.get_path('tt2_pack')+'/include/user_images.csv'

	names={}
	with open(CSV_Users) as csvfile:
	     reader = csv.DictReader(csvfile)
	     for row in reader:
	         names['s'+row['id_number']]=row['first_name']

	file_csv=open(CSV_Images,'w')

	BASE_PATH=rospack.get_path('tt2_pack')+'/src/dataBase2'
	SEPARATOR=","
	label = 1
	flag=False
	for dirname, dirnames, filenames in os.walk(BASE_PATH):
	    for subdirname in dirnames:
	        subject_path = os.path.join(dirname, subdirname)
	        for filename in os.listdir(subject_path):
	            abs_path = "%s/%s" % (subject_path, filename)
	            try:
	            	file_csv.write("%s%s%d%s%s\n" % (abs_path, SEPARATOR, label, SEPARATOR, names[subdirname]))
	            	flag=True
	            except:
	            	flag=False
	        if flag:
	        	label = label + 1
	file_csv.close()

#!/usr/bin/env python

import sys
import os.path

file_csv=open('new_csv.csv','w')

if __name__ == "__main__":

    BASE_PATH=os.getcwd()
    SEPARATOR=","
    names={'s1':'Balam','s2':'Alex','s3':'Brenda','s4':'Dani','s5':'Fortanel','s6':'Hector','s7':'Marvin','s8':'Lalo','s9':'Popoca','s10':'Rosey','s11':'Alex2'}

    label = 0
    for dirname, dirnames, filenames in os.walk(BASE_PATH):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                abs_path = "%s/%s" % (subject_path, filename)
                file_csv.write("%s%s%d%s%s\n" % (abs_path, SEPARATOR, label, SEPARATOR, names[subdirname]))
            label = label + 1
file_csv.close()

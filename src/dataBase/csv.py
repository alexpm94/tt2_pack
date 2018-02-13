#!/usr/bin/env python

import sys
import os.path

file_csv=open('new_csv.csv','w')

if __name__ == "__main__":

    BASE_PATH=os.getcwd()
    SEPARATOR=","

    label = 0
    for dirname, dirnames, filenames in os.walk(BASE_PATH):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                abs_path = "%s/%s" % (subject_path, filename)
                file_csv.write("%s%s%d\n" % (abs_path, SEPARATOR, label))
            label = label + 1
file_csv.close()

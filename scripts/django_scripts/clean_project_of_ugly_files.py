#!/usr/bin/env python

#this script removes all .pyc and .py~ files from django projects, making
#them easier to navigate and work in


import sys, os, re, unittest

HOMEPATH = os.path.expanduser('~')
DJANGO_PATH = os.path.join(HOMEPATH, 'django_practice')
PROJECT_PATH = os.getcwd()

assert os.path.isdir(PROJECT_PATH), "{PROJECT_PATH} isn't a real directory".format(PROJECT_PATH=PROJECT_PATH)

higher_path, current_folder = os.path.split(PROJECT_PATH)

assert higher_path == DJANGO_PATH, "You need to call this script in the main project folder that contains manage.py"


for root, dirs, files in os.walk(PROJECT_PATH):
    for f in files:
        if f.endswith(('pyc', 'py~',)):
            file_to_remove = root + '/' + f
            # print 'removing file: ', file_to_remove
            os.remove(file_to_remove)

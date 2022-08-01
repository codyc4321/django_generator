#!/usr/bin/env python

# in .bashrc:
# port() { $PATH_TO_SCRIPT "$@" ;}

# run django runserver to any port like:
# port 8001


import sys, subprocess

port = sys.argv[1]

def call_sp(command, **arg_list):
    p = subprocess.Popen(command, shell=True, **arg_list)
    p.communicate()

call_sp('python manage.py runserver 127.0.0.1:{}'.format(port))
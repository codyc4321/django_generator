#!/usr/bin/env python

import time, subprocess, os

CWD = os.getcwd()

def call_sp(command, **arg_list):
    p = subprocess.Popen(command, shell=True, **arg_list)
    p.communicate()

call_sp("{}/robots/reset.py".format(CWD))
time.sleep(3)
call_sp("{}/robots/app_writer.py".format(CWD))
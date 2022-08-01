#!/usr/bin/env python

import time, subprocess, os
CWD = os.getcwd()


def call_sp(command, **arg_list):
    p = subprocess.Popen(command, shell=True, **arg_list)
    p.communicate()


fake            = "{}/main/scripts".format(CWD)
template_fake   = "{}/templates/scripts".format(CWD)

print fake 
print template_fake
call_sp("rm -rf {}".format(fake))
time.sleep(2)
call_sp("rm -rf {}".format(template_fake))
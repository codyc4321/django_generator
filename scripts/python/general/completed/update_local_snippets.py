#!/usr/bin/env python

import os, sys, re, subprocess, time

HOMEPATH     = os.getenv("HOME")
SILO_PATH_AT_WORK = os.path.join(HOMEPATH, 'django_practice/atom_files')
SILO_PATH_AT_HOME = os.path.join(HOMEPATH, 'django_practice/atom')
ATOM_PATH = os.path.join(HOMEPATH, '.atom')

ATOM_FILES = ['snippets.cson', 'config.cson']

#----------------------------------------------------------------------------------------------------

def call_sp(command, **arg_list):
    p = subprocess.Popen(command, shell=True, **arg_list)
    p.communicate()


#------------------------------------------------------------------------------------------------------------------------

def read_content(the_file):
    f = file(the_file, 'r')
    content = f.read()
    f.close()
    return content

#------------------------------------------------------------------------------------------------------------------------

def write_content(the_file, content):
    f = file(the_file, 'w')
    f.write(content)
    f.close

#-------------------------------------------------------------------------------------------------------------------------

if os.path.isdir(SILO_PATH_AT_WORK):
    THISPATH = SILO_PATH_AT_WORK
else:
    THISPATH = SILO_PATH_AT_HOME


d = {'cwd': THISPATH}
call_sp('git pull', **d)
time.sleep(3.5)

for f in ATOM_FILES:
    this_silo_file_path = os.path.join(THISPATH, f)
    content = read_content(this_silo_file_path)
    this_atom_file_path = os.path.join(ATOM_PATH, f)
    write_content(this_atom_file_path, content)

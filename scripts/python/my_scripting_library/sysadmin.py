
import os, sys, re, requests, optparse, subprocess, time

HOMEPATH = os.path.expanduser('~')
PROJECT_PATH = os.path.join(HOMEPATH, "django_practice")


HOMEPATH = os.path.expanduser('~')

CWD = os.getcwd()


#----------------------------------------------------------------------------------------------------

def call_sp(command, **arg_list):
    p = subprocess.Popen(command, shell=True, **arg_list)
    p.communicate()
    
#------------------------------------------------------------------------------------------------------------------------

def read_lines(the_file):
    f = file(the_file, 'r')
    content = f.readlines()
    f.close()
    return content

#------------------------------------------------------------------------------------------------------------------------

def read_content(the_file):
    f = file(the_file, 'r')
    content = f.read()
    f.close()
    return content

#------------------------------------------------------------------------------------------------------------------------

def write_lines(the_file, lines):
    f = file(the_file, 'w')
    f.writelines(lines)
    f.close

#------------------------------------------------------------------------------------------------------------------------

def write_content(the_file, content):
    f = file(the_file, 'w')
    f.write(content)
    f.close

#------------------------------------------------------------------------------------------------------------------------

def append_lines(the_file, lines):
    f = file(the_file, 'a')
    f.writelines(lines)
    f.close

#------------------------------------------------------------------------------------------------------------------------

def append_content(the_file, content):
    f = file(the_file, 'a')
    f.write(content)
    f.close

#-------------------------------------------------------------------------------------------------------------------------

def clear_content(the_file):
    f = file(the_file, 'w')
    f.write('')
    f.close

#-------------------------------------------------------------------------------------------------------------------------

def clear_folder(dirpath):
    for root, dirs, files in os.walk(dirpath):
        for f in files:
            fullpath = os.path.join(root, f)
            clear_content(fullpath)

#-------------------------------------------------------------------------------------------------------------------------

def ensure_startswith(string, starter):
    if string.startswith(starter):
        return string
    else:
        return starter + string
        
#----------------------------------------------------------------------------------------------------

def ensure_endsswith(string, ender):
    if string.endswith(ender):
        return string
    else:
        return string + ender

#!/usr/bin/env python

import os, sys, time, subprocess
from os.path import expanduser

HOME = expanduser('~')

SCRIPTS = os.path.join(HOME, 'scripts')

def call_sp(command, **arg_list):
    #run that beast
    p = subprocess.Popen(command, shell=True, **arg_list)
    p.communicate()



def get_project_path():
    i = 0
    for root, dirs, files in os.walk(HOME):
        if i >= 2:
            return "couldnt find project path"
        i += 1
        for this_dir in dirs:
            if this_dir == "django_practice":
                return os.path.join(HOME, "django_practice")
        for this_dir in dirs:
            if this_dir == "projects":
                return os.path.join(HOME, "projects")

def update_projects(project_path):
    i = 0
    for root, dirs, files in os.walk(project_path):
        for this_dir in dirs:
            if this_dir.startswith("."):
                continue
            full_path = os.path.join(root, this_dir)
            print full_path
            time.sleep(2)

            is_git_project = False

            for subroot, subdirs, subfiles in os.walk(full_path):
                if not ".git" in subdirs:
                    break
                else:
                    is_git_project = True
                subdirs[:] = []

            if not is_git_project:
                continue

            d = {'cwd': full_path}
            print 'git pull from {}'.format(full_path)
            call_sp('git pull', **d)
            time.sleep(2)
        dirs[:] = []

ppath = get_project_path()
update_projects(ppath)
d = {'cwd': SCRIPTS}
print 'git pull from {}'.format(SCRIPTS)
call_sp('git pull', **d)

#!/usr/bin/env python

import os, sys, time, subprocess
from os.path import expanduser

HOME = expanduser('~')

def call_sp(command, **arg_list):
    #run that beast
    p = subprocess.Popen(command, shell=True, **arg_list)
    p.communicate()


def get_project_path():
    i = 0
    for root, dirs, files in os.walk(HOME):
        if i >= 2:
            return os.path.join(HOME, "projects")
        i += 1
        for this_dir in dirs:
            if this_dir == "django_practice":
                return os.path.join(HOME, "django_practice")

def update_projects(home_path):
    i = 0
    for root, dirs, files in os.walk(home_path):
        for this_dir in dirs:
            if this_dir.startswith("."):
                continue
            full_path = os.path.join(root, this_dir)
            print full_path
            time.sleep(2)

            is_git_project = False
            j = 0
            for subroot, subdirs, subfiles in os.walk(full_path):
                if j >= 1:
                    break
                j += 1
                if not ".git" in subdirs:
                    break
                else:
                    is_git_project = True

            if not is_git_project:
                continue

            d = {'cwd': full_path}
            print 'git pull from {}'.format(full_path)
            call_sp('git pull', **d)
            time.sleep(2)
            call_sp('git add -A', **d)
            call_sp('git commit -m "automatic update"', **d)
            call_sp('git push', **d)
        dirs[:] = []

ppath = get_project_path()
update_projects(ppath)

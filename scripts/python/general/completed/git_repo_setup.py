#!/usr/bin/env python

import subprocess
import os
import sys
import optparse
import time

"""

calling from script:
./git_cloner.py projectname branchname
to make a new advantage branch say ./git_cloner.py advantage dev

interactive:
just run ./git_cloner.py

"""

cwd = os.getcwd()

print cwd

d = {'cwd': cwd}

print d

if len(sys.argv) == 2:
    project = sys.argv[1]



if len(sys.argv) < 2:
    while True:
        project = raw_input('Enter a project name (i.e., transmorgify):\n')
        if not project:
            continue
        break



def call_sp(command, **arg_list):
    p = subprocess.Popen(command, shell=True, **arg_list)
    p.communicate()



call_sp('mkdir %s' % project, **d)
project_path = curr_w_d + '/' + project
d['cwd'] = project_path
call_sp('git init', **d)
time.sleep(1)
git_string = 'git remote add origin git@bitbucket.org:codyc54321/{}.git'.format(project, d['cwd'])
time.sleep(5)
call_sp(git_string)
print "\n{}\n\n".format(git_string)
time.sleep(1)
gitignore_path  = os.path.join(project_path, '.gitignore')
if not os.path.exists(gitignore_path):
    call_sp('touch .gitignore', **d)
    time.sleep(0.3)
    gitignore_string = "*.pyc\n*.py~\n.idea/*\n*migrations*\ndb.sqlite3"
    call_sp('echo "{}" > ./.gitignore'.format(gitignore_string), **d)
    time.sleep(0.1)
call_sp('git add -A',   **d)
# call_sp('git commit -m "initial commit for {}"'.format(project), **d)
# call_sp('git push -u origin master', **d)

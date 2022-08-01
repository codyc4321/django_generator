#!/usr/bin/env python

import subprocess
import sys
import time
from os.path import expanduser

home_path = expanduser('~')
project_path = home_path + '/projects'


d = {'cwd': ''}



#calling from script:
# ./git_cloner.py projectname branchname
# to make a new branch say ./git_cloner.py project branchname

#interactive:
# just run ./git_cloner.py




if len(sys.argv) == 3:
    project = sys.argv[1]
    branch  = sys.argv[2]



if len(sys.argv) < 3:
    while True:
        project = raw_input('Enter a project name (i.e., advantage):\n')
        if not project:
            continue
        break

    while True:
        branch = raw_input('Enter a branch name (i.e., dev):\n')
        if not branch:
            continue
        break




def call_sp(command, **arg_list):
    p = subprocess.Popen(command, shell=True, **arg_list)
    p.communicate()




print "making new branch \"%s\" in project \"%s\"" % (branch, project)




this_project_path = '%s/%s' % (project_path, project)
branch_path  = '%s/%s' % (this_project_path, branch)

d['cwd'] = project_path
call_sp('mkdir %s' % branch, **d)
d['cwd'] = branch_path
git_string = 'git clone ssh://git@git/home/git/repos/{}.git {}'.format(project, d['cwd'])
#see what you're doing to maybe need to cancel
print '\n'
print "{}\n\n".format(git_string)
call_sp(git_string)
time.sleep(30)
call_sp('git checkout dev', **d)
time.sleep(2)
call_sp('git checkout -b {}'.format(branch), **d)
time.sleep(5)
call_sp('sudo ln -sf ../../bridge/dev/ bridge',   **d)
call_sp('sudo ln -sf ../../central/dev/ central', **d)
call_sp('sudo ln -sf ../../library/dev/ library', **d)
print this_project_path
print 'cp {}/dev/settings.py {}/settings.py'.format(this_project_path, branch_path)
print 'dont forget "git push -u origin {}"'.format(branch)



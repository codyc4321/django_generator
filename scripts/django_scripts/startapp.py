#!/usr/bin/env python

"""starts app, registers app name in settings.py, makes default urls and views files, adds internal templates folder"""


import re, os, sys, subprocess, time
from os.path import expanduser

home_path = expanduser('~')
project_path = home_path + '/projects'

def read_file(filename):
    # print filename
    f = file(filename, 'r')
    content = f.read()
    return content

def write_file(filename, content):
    f = file(filename, 'w')
    f.write(content)
    f.close()

def get_settings_path(starting_dir):
    settings_path = None
    # print '{}/{}'.format(project_path, project)
    for (dirpath, dirnames, filenames) in os.walk(starting_dir):
        if 'settings.py' in filenames:
            settings_path = dirpath + '/settings.py'
            break
    return settings_path

def call_sp(command, *args, **kwargs):
    sp = subprocess.Popen(command, shell=True, *args, **kwargs)
    sp.communicate()


current=os.getcwd()

#get project name
rgx = ".*/(?P<project>\w+)"
match = re.search(rgx, current)
project = match.group('project')

app_name = sys.argv[1]

call_sp('python manage.py startapp {}'.format(app_name))
time.sleep(2)

#get content of settings.py to insert the new app name
settings_path = get_settings_path(current)
settings_content = read_file(settings_path)

#insert the app name
rgx = "INSTALLED_APPS.*?(?=\))"
match = re.search(rgx, settings_content, re.DOTALL)
start_string = match.group()
new_string = start_string + '    \'' + app_name + "',\n"
text, n = re.subn(rgx, new_string, settings_content, flags=re.DOTALL)
write_file(settings_path, text)

app_path = current + '/' + app_name

#make urls.py file
urls_path = app_path + '/urls.py'
urls_payload = "from django.conf.urls import patterns, include, url\n\nfrom {app_name} import views\n\nurlpatterns = patterns('',  \
          \n    url(r'^$',          views.index,             name='index'".format(app_name=app_name)
write_file(urls_path, urls_payload)

#make views.py file
views_path = app_path + '/views.py'
views_payload ="\
from django.shortcuts   import render, render_to_response, redirect\nfrom django.http        import HttpResponse, HttpResponseRedirect\n\n \
def index(request):\n \
    return render(request, {app_name}/index.html, locals())".format(app_name=app_name)
write_file(views_path, views_payload)

#make templates folder
template_dir = os.path.join(app_path + '/' + 'templates' + '/' + app_name)
os.makedirs(template_dir)

index_template_path = template_dir + '/index.html'
template_payload = "you got an index for app '{}'".format(app_name)
write_file(index_template_path, template_payload)

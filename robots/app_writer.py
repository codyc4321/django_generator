#!/usr/bin/env python

import os, subprocess, sys, re, requests, os

""" need to change - to _ (dash to underscore) in the path name or you get error"""
#at home
# sys.path.append('/home/cchilders/projects/scriptcity')

BASE_DIR = os.getcwd()

APP_DIR = BASE_DIR + '/scripts'

TEST_DIR = BASE_DIR + '/main'

TEMPLATE_DIR = BASE_DIR + '/templates'

VIEWS_PAYLOAD   = "from django.shortcuts import render\n\n"

URLS_PAYLOAD    = "from django.conf.urls import patterns, include, url\n\nurlpatterns = patterns('',\n\n)"

PAYLOADS        = {'init': '', 'urls': URLS_PAYLOAD, 'views': VIEWS_PAYLOAD, 'template': ''}

API_URL = "http://hilite.me/api"

payload = { "code": "#!/usr/bin/env python\ndef func(param):\n    return fake",
            "lexer": "python",
            "style": "",
            "linenos": "True",
            "divstyles": "",}

lexer_dict = {'.py': 'python', '.sh': 'bash', '.rb': 'rb'}

#-----------------------------------------------------------------------------------------------------------------------

def call_sp(command, **arg_list):
    p = subprocess.Popen(command, shell=True, **arg_list)
    p.communicate()

#-----------------------------------------------------------------------------------------------------------------------

def read_content(the_file):
    f = file(the_file, 'r')
    content = f.read()
    f.close()
    return content

#-----------------------------------------------------------------------------------------------------------------------

def read_file_lines(the_file):
    f = file(the_file, 'r')
    content = f.readlines()
    f.close()
    return content
#-----------------------------------------------------------------------------------------------------------------------

def write_content(the_file, content):
    f = file(the_file, 'w')
    f.write(content)
    f.close

#-----------------------------------------------------------------------------------------------------------------------

def append_content(the_file, content):
    f = file(the_file, 'a')
    f.write(content)
    f.close

#-----------------------------------------------------------------------------------------------------------------------

def insert_parent_template_payload(filepath, payload):
    try:
        content     = read_content(filepath)
        if content.find(payload) != -1:
            return 0
        append_content(filepath, payload)
    except:
        write_content(filepath, payload)

#-----------------------------------------------------------------------------------------------------------------------

def insert_url_pattern_payload(filepath, payload):
    content         = read_content(filepath)
    if content.find(payload) != -1:
        return 0
    rgx             = "urlpatterns = .*(?=\))"
    match           = re.search(rgx, content, re.DOTALL)
    start_string    = match.group()
    new_string      = start_string + payload
    new_content     = re.sub(rgx, new_string, content, flags=re.DOTALL)
    write_content(filepath, new_content)

#-----------------------------------------------------------------------------------------------------------------------

def insert_views_import_to_urls(filepath, payload):
    content         = read_content(filepath)
    if content.find(payload) != -1:
        return 0
    rgx             = "from django.conf.urls import patterns, include, url\n"
    match           = re.search(rgx, content, re.DOTALL)
    start_string    = match.group()
    new_string      = start_string + payload + '\n'
    new_content     = re.sub(rgx, new_string, content, flags=re.DOTALL)
    write_content(filepath, new_content)

#-----------------------------------------------------------------------------------------------------------------------

def insert_views_payload(filepath, payload):
    content         = read_content(filepath)
    if content.find(payload) != -1:
        return 0
    append_content(filepath, payload)

#-----------------------------------------------------------------------------------------------------------------------

def get_filename_from_path(filepath):
    rgx         = r".*/(.*)"
    match       = re.search(rgx, filepath)
    return  match.group(1)

#-----------------------------------------------------------------------------------------------------------------------

def check_for_hidden_files_or_dirs(filepath):
    rgx = r"/\."
    if re.search(rgx, filepath):
        return True
    else:
        if filepath.startswith('.'):
            return True
        else:
            return False

#-----------------------------------------------------------------------------------------------------------------------

def get_html_content(url, payload):
    session = requests.session()
    r       = requests.post(url, data=payload)
    return r.text

#-----------------------------------------------------------------------------------------------------------------------

if not os.path.isdir('{}/main/scripts'.format(BASE_DIR)):
    os.makedirs('{}/main/scripts'.format(BASE_DIR))


i = 0


FILENAMES = []


for root, dirs, files in os.walk(APP_DIR):

     # based on root: /home/cchilders/projects/scriptcity/scripts
    if check_for_hidden_files_or_dirs(root):
        continue

    for this_dir in dirs:
        this_dir = this_dir.replace("-", "_")

    # scripts
    this_root           = root.replace((BASE_DIR + '/'), '')
    this_root           = this_root.replace('-', '_')
    # /home/cchilders/projects/scriptcity/main/scripts
    new_dir_path        = os.path.join(TEST_DIR, this_root)
    # /home/cchilders/projects/scriptcity/templates/scripts
    new_template_dir    = os.path.join(TEMPLATE_DIR, this_root)

    if not os.path.isdir(new_dir_path):
        os.makedirs(new_dir_path)
    if not os.path.isdir(new_template_dir):
        os.makedirs(new_template_dir)

    # /home/cchilders/projects/scriptcity/templates/scripts/index.html
    index_template_path = os.path.join(new_template_dir, 'index.html')

    append_content(index_template_path, 'at the index for {}\n'.format(this_root))

    files_dict          = {}
    files_dict['init']  = new_dir_path + "/__init__.py"
    files_dict['urls']  = new_dir_path + "/urls.py"
    files_dict['views'] = new_dir_path + "/views.py"
    for key, value in files_dict.items():
        write_content(value, PAYLOADS[key])

    # scripts/index.html
    index_path_for_view = os.path.join(this_root, "index.html")
    view_payload = "\ndef index(request):\n\
    return render(request, '{}')\n\n".format(index_path_for_view)

    insert_views_payload(files_dict['views'], view_payload)

    # add 'from main.scripts import views'
    # main.scripts
    root_dot_path = 'main.' + this_root.replace('/', '.')
    underscore_only_root_dot_path = root_dot_path.replace('-', '_')
    url_views_import_payload = "from {} import views".format(underscore_only_root_dot_path)
    insert_views_import_to_urls(files_dict['urls'], url_views_import_payload)

    # add the index url pattern
    index_pattern_payload = "    url(r'^$',  views.index,     name='index'),\n"
    insert_url_pattern_payload(files_dict['urls'], index_pattern_payload)

    for this_dir in dirs:
        if check_for_hidden_files_or_dirs(this_dir):
            continue
        # say we start with python as the dir...
        real_path               = os.path.join(root, this_dir)              #  ~/projects/scriptcity/scripts/python
        underscore_path         = real_path.replace('-', '_')
        relative_path           = underscore_path.replace((BASE_DIR + '/'), '')   # scripts/python

        url_include_path        = relative_path.replace('/', '.')           # scripts.python

        template_reverse_path   = "main:" + (relative_path.replace('/', ':') + ':index') # main:scripts:python:index

        regex                   = '^{}/'.format(this_dir)

        this_dir = this_dir.replace("-", "_")
        urls_pattern_payload     = "    url(r'{regex}',  include('main.{url_include_path}.urls',  namespace='{this_dir}')),\n"\
                                  .format(regex=regex, url_include_path=url_include_path, this_dir=this_dir)

        parent_template_payload = "<p><a href=\"{{% url '{template_reverse_path}' %}}\">{this_dir}</a></p>\n"\
                                  .format(template_reverse_path=template_reverse_path, this_dir=this_dir)


        insert_url_pattern_payload(files_dict['urls'], urls_pattern_payload)
        insert_parent_template_payload(index_template_path, parent_template_payload)



    for this_file in files:
        FILENAMES.append(this_file)
        if check_for_hidden_files_or_dirs(this_file):
            continue

        real_path               = os.path.join(root, this_file) # ~/projects/scriptcity/scripts/python/fake.py
        real_path_underscore    = real_path.replace('-', '_')
        filename, extension     = os.path.splitext(real_path)   # ~/projects/scriptcity/scripts/python/fake, .py
        underscore_filename     = filename.replace("-", "_")
        if extension not in ['.py', '.sh', '.rb']:
            continue

        starter_r_path          = real_path_underscore.replace(BASE_DIR, '')
        relative_path           = starter_r_path[1:] # scripts/python/fake.py

        # make template_reverse_path
        rel                     = underscore_filename.replace(BASE_DIR, '')
        rel2                    = rel[1:]
        template_reverse_path   = 'main:' + rel2.replace('/', ':') # main:scripts:python:fake

        starter_t_path          = underscore_filename.replace(BASE_DIR, '') + '.html'
        relative_template_path  = starter_t_path[1:] # # scripts/python/fake.html
        desired_template_path   = TEMPLATE_DIR  + real_path.replace(BASE_DIR, '')
        filename_wo_path        = get_filename_from_path(underscore_filename)
        # ~/django_practice/scriptcity/templates/scripts/python/fake.html
        new_template_path_as_html = os.path.join(TEMPLATE_DIR, relative_template_path)

        #get hilite me content:
        content = read_content(real_path)
        payload = {}
        payload["code"]     = read_content(real_path)
        payload["lexer"]    = lexer_dict[extension]
        payload["style"]    = ""
        payload["divstyles"]= ""
        payload["linenos"]  = "y"
        highlighed_content  = get_html_content(API_URL, payload)

        new_template_path_as_html = new_template_path_as_html.replace('-', '_')
        write_content(new_template_path_as_html, highlighed_content)


        urls_pattern_payload     = "    url(r'^{filename}/$',  views.access_{filename},  name='{filename}'),\n"\
                                  .format(filename=filename_wo_path)

        parent_template_payload = "<p><a style=\"color:green\" href=\"{{% url '{template_reverse_path}' %}}\">{filename}</a></p>\n"\
                                  .format(template_reverse_path=template_reverse_path, filename=filename_wo_path)

        view_function_payload   = "def access_{filename}(request):\n    return render(request, '{template_path}')\n\n"\
                                  .format(filename=filename_wo_path, template_path=relative_template_path)

        insert_url_pattern_payload(files_dict['urls'], urls_pattern_payload)
        insert_views_payload(files_dict['views'], view_function_payload)
        insert_parent_template_payload(index_template_path, parent_template_payload)

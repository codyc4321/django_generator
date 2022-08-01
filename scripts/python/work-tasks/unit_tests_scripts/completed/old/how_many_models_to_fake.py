#!/usr/bin/env python

import re, subprocess, sys, os


"""see how many models I gotta make as fakes, may be faster to automate it

update: This was how I determined if to write the models by hand or not. I learned it'd be several thousand lines of repetitive stuff
"""

HOMEPATH = os.path.expanduser('~')
project_path = HOMEPATH + "/projects/advantage/unit_tests"

#------------------------------------------------------------------------------------------------------------------------

def read_file_lines(the_file):
    f = file(the_file, 'r')
    content = f.readlines()
    f.close()
    return content

#------------------------------------------------------------------------------------------------------------------------
    content = f.read()
    f.close()
    return content

#------------------------------------------------------------------------------------------------------------------------

def write_content(the_file, content):
    f = file(the_file, 'w')
    f.write(content)
    f.close

#------------------------------------------------------------------------------------------------------------------------

def write_lines(the_file, content):
    f = file(the_file, 'w')
    f.writelines(content)
    f.close
#------------------------------------------------------------------------------------------------------------------------

def append_content(the_file, content):
    f = file(the_file, 'a')
    f.write(content)
#------------------------------------------------------------------------------------------------------------------------

def clear_content(the_file):
    f = file(the_file, 'w')
    f.write('')
    f.close

#------------------------------------------------------------------------------------------------------------------------

def get_model_name_or_None(line):
    regex = r"^class\s+(\w+)\(models.Model"
    try:
        match = re.search(regex, line)
        return match.group(1)
    except:
        return None

#------------------------------------------------------------------------------------------------------------------------

def get_all_model_names(filepath):
    content = read_file_lines(filepath)
    name_info = {'file': filepath, 'modelnames': []}
    for line in content:
        name = get_model_name_or_None(line)
        if name:
            print 'name: ', name
            name_info['modelnames'].append(name)
    return name_info

#------------------------------------------------------------------------------------------------------------------------

def walk_advantage_and_gather_names(project_path):
    temp_file = '/tmp/all_model_names.txt'
    clear_content(temp_file)
    model_count = 0
    for root, dirs, files in os.walk(project_path):
        for this_file in files:
            this_path = os.path.join(root, this_file)
            names_info = get_all_model_names(this_path)
            if names_info['modelnames']:
                model_count += len(names_info['modelnames'])
                append_content(temp_file, str(names_info))
                append_content(temp_file, '\n\n')
    append_content(temp_file, '\nModels: {}'.format(model_count))


#------------------------------------------------------------------------------------------------------------------------

walk_advantage_and_gather_names(project_path)

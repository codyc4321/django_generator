#!/usr/bin/env python

import re, subprocess, sys, os
from os.path import expanduser

"""Generates ipython ready commands to test our models in the shell...be in the unit_tests project in shell"""


factory_path = "/home/cchilders/projects/advantage/unit_tests/testing/factories"

#------------------------------------------------------------------------------------------------------------------------

def read_file_lines(the_file):
    f = file(the_file, 'r')
    content = f.readlines()
    f.close()
    return content

#------------------------------------------------------------------------------------------------------------------------

def read_file_content(the_file):
    f = file(the_file, 'r')
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

def get_model_name_or_None(line):
    regex = r"^class\s+(\w+)\(DjangoModelFactory\)"
    try:
        match = re.search(regex, line)
        return match.group(1)
    except:
        return None

#------------------------------------------------------------------------------------------------------------------------

def get_all_model_names_as_commands(filepath):
    content = read_file_lines(filepath)
    commands = []
    for line in content:
        name = get_model_name_or_None(line)
        if name:
            commands.append('from testing.factories import ' + name + '\nx = {}.build_batch(7)\nx\n\n'.format(name))
    return commands

#------------------------------------------------------------------------------------------------------------------------

def walk_advantage_and_gather_names(project_path):
    for root, dirs, files in os.walk(project_path):
        all_commands = []
        for this_file in files:
            if this_file in  ["__init__.py", "extras.py"]:
                continue
            this_path = os.path.join(root, this_file)
            new_commands = get_all_model_names_as_commands(this_path)
            for command in new_commands:
                all_commands.append(command)
        dirs[:] = []
    content = "\n".join(all_commands)
    write_content('/home/cchilders/unit_tests_auto/tmp/import_commands.txt', content)

#------------------------------------------------------------------------------------------------------------------------

# HOME = expanduser('~')
#
# fullpath = os.path.join(HOME, sys.argv[1])
#
# write_content('/tmp/modelnames.txt', str(names))

walk_advantage_and_gather_names(factory_path)
print "check /home/cchilders/unit_tests_auto/tmp/import_commands.txt"

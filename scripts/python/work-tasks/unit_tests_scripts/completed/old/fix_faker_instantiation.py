#!/usr/bin/env python

import re, subprocess, sys, os

"""throw away to correct FAKER initialization"""

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

def replace_for_each_file_in_factories(filepath):
    file_content = read_file_content(filepath)
    regex = r"FAKER\s*=\s*Faker()"
    match = re.search(regex, file_content, re.DOTALL)
    try:
        string_to_sub = match.group()
        new_string    = "FAKER = Faker(locale='en_US')"
        text = re.sub(regex, new_string, file_content, flags=re.DOTALL)
        write_content(filepath, text)
    except:
        pass

#------------------------------------------------------------------------------------------------------------------------

def walk_factories_and_fix_FAKER(factory_path):
    for root, dirs, files in os.walk(factory_path):
        for this_file in files:
            if this_file == "__init__.py":
                continue
            this_path = os.path.join(root, this_file)
            replace_for_each_file_in_factories(this_path)
        dirs[:] = []

#------------------------------------------------------------------------------------------------------------------------

walk_factories_and_fix_FAKER(factory_path)

#!/usr/bin/env python

import re, subprocess, sys, os

"""
as I check my autowritten models for accuracy and change details, registers them in the __all__ by rewriting all 
files in the appropriate folder. It's cool to watch it work
"""

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

def get_model_name_or_None(line):
    regex = r"^class\s+(\w+)\("
    try:
        match = re.search(regex, line)
        return match.group(1)
    except:
        return None

#------------------------------------------------------------------------------------------------------------------------

def get_all_model_names(filepath):
    content = read_file_lines(filepath)
    names = []
    for line in content:
        name = get_model_name_or_None(line)
        if name:
            names.append(name)
    name_string = str(names)
    name_string = name_string.replace('[', '')
    name_string = name_string.replace(']', '')
    if len(names) == 1:
        name_string += ','
    return names
    # print name_string
    # return name_string

#------------------------------------------------------------------------------------------------------------------------

def write_names_to_magic_all_list_in_factory(filepath):

    def pretty_tuple_maker(list):
        string = ""
        for i, item in enumerate(list):
            print i, item
            if i % 5 == 0 and not i == 0:
                string += "\n    '" + str(list[i]) + "', "
            else:
                if (i + 1) % 5 == 0:
                    string += "'" + str(list[i]) + "',"
                else:
                    string += "'" + str(list[i]) + "', "
        return string

    names = get_all_model_names(filepath)
    rgx = "__all__\s*=\s*\((?P<entrails>.*?)(?=\))"
    file_content = read_file_content(filepath)
    try:
        match = re.search(rgx, file_content, re.DOTALL)
        string_to_sub = match.group()
        new_string    = "__all__ = (\n    " + pretty_tuple_maker(names) + "\n"
        text = re.sub(rgx, new_string, file_content, flags=re.DOTALL)
        write_content(filepath, text)
    except AttributeError:
        print "AttributeError"
        try:
            rgx = "from faker import Faker"
            match = re.search(rgx, file_content, re.DOTALL)
            start_string = match.group()
            new_string = start_string + '\n\n' +  "__all__ = (\n    " + names + "\n)"
            print 'in 1: ', new_string
            text = re.sub(rgx, new_string, file_content, flags=re.DOTALL)
            write_content(filepath, text)
        except AttributeError:
            print "AttributeError"
            pass







#------------------------------------------------------------------------------------------------------------------------

def walk_factories_and_update_names(factory_path):
    for root, dirs, files in os.walk(factory_path):
        for this_file in files:
            if this_file == "__init__.py":
                continue
            this_path = os.path.join(root, this_file)
            write_names_to_magic_all_list_in_factory(this_path)
        dirs[:] = []

#------------------------------------------------------------------------------------------------------------------------

walk_factories_and_update_names(factory_path)

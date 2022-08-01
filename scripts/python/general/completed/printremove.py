#!/usr/bin/env python

import re, sys
from os import listdir
from os.path import isfile, join


def read_content_to_linelist(the_file):
    try:
        f = file(the_file, 'r')
        content = f.readlines()
        f.close()
        return content
    except IOError:
        return 0

#-----------------------------------------------------------------------------------------------------------------------

def write_content(the_file, content):
    f = file(the_file, 'w')
    f.write(content)
    f.close

#-----------------------------------------------------------------------------------------------------------------------

def remove_print(linelist):
    string = ""
    num = 1
    for line in linelist[:]:
        num += 1
        if re.match(r"\s*[#]*\s*print", line):
            linelist.remove(line)
    for line in linelist:
        string += line
    return string

#-----------------------------------------------------------------------------------------------------------------------

def get_only_files(dir):
    onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f))]
    correct_file_names = get_the_file_names(onlyfiles)
    final_names = [dir + '/' + f for f in correct_file_names]
    return final_names

#-----------------------------------------------------------------------------------------------------------------------

def get_only_dirs(the_dir):
    try:
        all_items = listdir(the_dir)
    except OSError:
        return 0
    dirs = [the_dir + '/' + f for f in all_items if not re.search('\..*', f)]
    dirs.append(the_dir)
    return dirs

#------------------------------------------------------------------------------------------------------------------------

def get_files_to_check(dirs_to_check):
    total_files = []
    while dirs_to_check:
        for d in dirs_to_check:
            try:
                listdir(d)
            except OSError:
                total_files.append(d)
                dirs_to_check.remove(d)
                continue
            dirs_to_add = get_only_dirs(d)
            files_to_add = get_only_files(d)
            dirs_to_check.remove(d)
            if dirs_to_add:
                for dir_to_add in dirs_to_add:
                    dirs_to_check.append(dir_to_add)
            if files_to_add:
                for file_to_add in files_to_add:
                    total_files.append(file_to_add)
            dirs_to_check.remove(d)

    return total_files

def get_the_file_names(file_list):
    files = []
    for file in file_list:
        the_file = re.sub('\n', '', file)
        files.append(the_file)
    return files

#------------------------------------------------------------------------------------------------------------------------

def remove_print_for_file(filename):
    lines = read_content_to_linelist(filename)
    content = remove_print(lines)
    write_content(filename, content)

#------------------------------------------------------------------------------------------------------------------------

def get_all_files_in_dir(starting_dir):
    dirs_to_check = get_only_dirs(starting_dir)
    files = get_files_to_check(dirs_to_check)
    return files

#------------------------------------------------------------------------------------------------------------------------

def remove_print_for_all_files(files):
    for f in files:
        remove_print_for_file(f)
    return 1

#------------------------------------------------------------------------------------------------------------------------


#the meat

if len(sys.argv) == 2:
    the_arg = sys.argv[1]
    try:
        items = listdir(the_arg)
        the_type = 'dir'
    except OSError:
        the_type = 'file'


if len(sys.argv) != 2:
    while True:
        the_arg = raw_input('Enter a directory  or file name (i.e., "/home/user/projects/advantage/dev"):\n')
        if not the_arg:
            continue
        break
    try:
        items = listdir(the_arg)
        the_type = 'dir'
    except OSError:
        the_type = 'file'


if the_type == 'dir':
    while True:
        confirm = raw_input("{} is a directory...are you sure you wanna remove all prints under it? (y/n)\n".format(the_arg))
        if confirm == 'y':
            files = get_all_files_in_dir(the_arg)
            remove_print_for_all_files(files)
            break
        elif confirm == 'n':
            sys.exit()
        else:
            continue
elif the_type == 'file':
    while True:
        confirm = raw_input("Are you sure you wanna remove all prints in {}? (y/n)\n".format(the_arg))
        if confirm == 'y':
            remove_print_for_file(the_arg)
            break
        elif confirm == 'n':
            sys.exit()
        else:
            continue
    remove_print_for_file(the_arg)
else:
    raise Exception

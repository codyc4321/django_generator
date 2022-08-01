#!/usr/bin/env python

import re, sys, subprocess, time
from os import listdir
from os.path import exists, isfile, join


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

def remove_line(linelist, line_to_match):
    string = ""
    num = 1
    rgx = "\s*" + line_to_match
    for line in linelist[:]:
        num += 1
        if re.match(r"{}".format(rgx), line):
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
    dirs = [the_dir + '/' + f for f in all_items if not re.search('\..*', f)
                                        # and not f in files
            ]
    dirs.append(the_dir)
    return dirs

#------------------------------------------------------------------------------------------------------------------------

def get_files_to_check(dirs_to_check):
    total_files = []
    while dirs_to_check:
        for d in dirs_to_check:
            try:
                items = listdir(d)
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
        # time.sleep(8)
    return total_files

def get_the_file_names(file_list):
    files = []
    for file in file_list:
        the_file = re.sub('\n', '', file)
        files.append(the_file)
    return files

#------------------------------------------------------------------------------------------------------------------------

def remove_line_for_file(filename, rgx):
    lines = read_content_to_linelist(filename)
    content = remove_line(lines, rgx)
    write_content(filename, content)

#------------------------------------------------------------------------------------------------------------------------

def remove_line_for_all_files(files, rgx):
    for f in files:
        remove_line_for_file(f, rgx)
    return 1

#------------------------------------------------------------------------------------------------------------------------


if len(sys.argv) == 3:
    the_arg = sys.argv[1]
    try:
        items = listdir(the_arg)
        the_type = 'dir'
    except OSError:
        the_type = 'file'
    the_line = sys.argv[2]







if the_type == 'dir':
    while True:
        confirm = raw_input("{} is a directory...are you sure you wanna remove all instances of '{}' in all files under it? (y/n)\n".format(the_arg, the_line))
        if confirm == 'y':
            files = get_all_files_in_dir(the_arg)
            remove_line_for_all_files(files, the_line)
            break
        elif confirm == 'n':
            sys.exit()
        else:
            continue
elif the_type == 'file':
    while True:
        confirm = raw_input("Are you sure you wanna remove all instances of '{}' in {}? (y/n)\n".format(the_line, the_arg))
        if confirm == 'y':
            remove_line_for_file(the_arg, the_line)
            break
        elif confirm == 'n':
            sys.exit()
        else:
            continue
    remove_line_for_file(the_arg, the_line)
else:
    raise Exception

#!/usr/bin/env python



# first argument should be path to count from, as in 'home/username/projects/advantage'


import sys, subprocess, re, time, string, datetime
from os.path import exists, isfile, join, expanduser, isdir
from os import listdir

alpha = string.ascii_lowercase
alpha_up = string.ascii_uppercase



home_path       = expanduser('~')
projects_path   =home_path + '/projects'


#------------------------------------------------------------------------------------------------------------------------

def call_sp(command, **arg_list):
    p=subprocess.Popen(command, shell=True, **arg_list)
    p.communicate()

#------------------------------------------------------------------------------------------------------------------------

def get_the_file_names(file_list):
    files = []
    for file in file_list:
        the_file = re.sub('\n', '', file)
        files.append(the_file)
    return files

#------------------------------------------------------------------------------------------------------------------------

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
                                        and not the_dir + f == '/home/cchilders/advantage/dev/central'
                                        and not the_dir + f == '/home/cchilders/advantage/dev/library'
                                        and not the_dir + f == '/home/cchilders/advantage/dev/bridge'
            ]
    return dirs

#-----------------------------------------------------------------------------------------------------------------------

def screen_filetype(filenames, desired_filetypes):
    desired_files = []
    print "\n\n\n"
    print desired_filetypes
    print "filetypes in screen filetpye ^^"
    for f in filenames:
        filetype = re.search('.(\w+)$', f).group(1)
        print 'filetype: {}'.format(filetype)
        if filetype in desired_filetypes:
            desired_files.append(f)
    return desired_files

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
            # print 'total files'
            # print total_files
            dirs_to_add = get_only_dirs(d)
            files_to_add = get_only_files(d)
            dirs_to_check.remove(d)
            if dirs_to_add:
                for dir_to_add in dirs_to_add:
                    dirs_to_check.append(dir_to_add)
            if files_to_add:
                for file_to_add in files_to_add:
                    total_files.append(file_to_add)
    return total_files




desired_filetypes = []


if len(sys.argv) >= 3:
    starting_dir = sys.argv[1]
    for index, arg in enumerate(sys.argv):
        print index, arg
        if index == 0 or index == 1:
            continue
        desired_filetypes.append(arg)



if len(sys.argv) == 2:
    starting_dir = sys.argv[1]
    while True:
        filetypes = raw_input('Enter some filetypes to grab separated by spaces:\n')
        if filetypes:
            desired_filetypes.append(filetypes.split())
            break
        elif filetype == '':
            continue

if len(sys.argv) == 1:
    while True:
        starting_dir = raw_input('Enter a starting dir:\n')
        if not starting_dir:
            continue
        else:
            break
    while True:
        filetypes = raw_input('Enter some filetypes to grab separated by spaces:\n')
        if filetypes:
            desired_filetypes.append(filetypes.split())
            break
        elif filetype == '':
            continue

print "desired filetypes:"
print desired_filetypes

if type(desired_filetypes[0]) == type([]):
    desired_filetypes = desired_filetypes[0]
print "desired filetypes:"
print desired_filetypes

dirs_to_check = get_only_dirs(starting_dir)

files = get_files_to_check(dirs_to_check)

desired_files = screen_filetype(files, desired_filetypes)
print desired_files

def get_timestamp():
    timestamp = ""
    now = datetime.datetime.now()
    month = now.strftime("%m")
    if month[0] == '0':
        month = month[1]
        timestamp += month + now.strftime("-%d-%y_%H:%M:%S")
    else:
        timestamp += now.strftime("%m-%d-%y_%H:%M:%S")
    return timestamp

timestamp = get_timestamp()
filetypes_string = ",".join(desired_filetypes)
desired_files_string = "\n".join(desired_files)
print desired_files_string
new_filename = "filetype-search_{}".format(timestamp)
call_sp('echo "files ending in {} on {}:\n\n{}" > /home/cchilders/Documents/{}.txt'.format(filetypes_string, timestamp, desired_files_string, new_filename))
call_sp('cat /home/cchilders/Documents/{}.txt'.format(new_filename))

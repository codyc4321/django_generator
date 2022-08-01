#!/usr/bin/env python

#search_replace.py allows you to change settings in all Django files in a certain project at once, with a few clicks. It's nice enough to even back your files up

#Program is mostly self explanatory

#Setting to replace literally means the setting. 

#For file '/home/cchilders/scripts/settings.py' with text

# 'BREAKFAST':  'waffles'

#is an example:
'''
#What setting do you want to replace?
#BREAKFAST
#
#Path to start from? (hit enter to start from home)
#scripts
#
#Full path: /home/cchilders/scripts
#
#Search by certain filename? (like 'settings.py') [TAKES ANY REGEX]
#settings*
#
#Is this the correct match?
#
#'BREAKFAST':  'waffles'
#
#enter 'y' or 'x' to exit this file
#y
#
#What do you want to substitute in?
#muffins
#
#will replace  "waffles" with "muffins" for setting "BREAKFAST"
#
#options work like: ./search_replace -m c
#or
#                   ./search_replace -m s
#
#can be ran as      ./search_replace setting filepath filename
#or
#                   ./search_replace setting filepath filename replacement
#
#please leave blank filepath or filename as ''
'''
#
#
#Turning on safe mode is annoying but useful for a few important files
#
#
#Turning cowboy mode on flys through and prints results before a confirmation, so if you trust yourself just 1 more button click to change all settings.
#Don't worry, it backs up all your files!

# slow
# ./search_replace.py,
# ./search_replace.py -m s,

# fast
# ./search_replace.py -m c,
# ./search_replace.py setting filepath filename,
# ./search_replace.py setting '' '',
# ./search_replace.py setting filepath filename replacement


import os
import subprocess
import sys
import re
import optparse


home_path = os.path.expanduser("~")




class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


mode =          None

parser = optparse.OptionParser()
parser.add_option('-m', '--mode', dest='mode', help='"c" for cowboy, "s" for safe')

(options, args) = parser.parse_args()

if options.mode == 'c':
    mode =  "cowboy"
elif options.mode == 's':
    mode =  "safe"
else:
    mode = "normal"

#------------------------------------------------------------------------------------------------------------------------

def check_mode():
    setting =       None
    filepath =      None
    filename =      None
    replacement =   None

    if len(sys.argv) < 4:
        interactive = True

    if len(sys.argv) == 4:
        interactive = False
        setting = sys.argv[1]
        if sys.argv[2] == '':
            filepath = home_path
        else:
            filepath = home_path + "/" + sys.argv[2]
        filename = sys.argv[3]

    if len(sys.argv) == 5:
        interactive = False
        setting = sys.argv[1]
        if sys.argv[2] == '':
            filepath = home_path
        else:
            filepath = home_path + "/" + sys.argv[2]
        filename = sys.argv[3]
        replacement = sys.argv[4]

    print ''

    if mode == 'cowboy':
        print '\nCowboy mode activated\n'
    if mode == 'safe':
        print '\nSafe mode activated\n'


    return (setting, filepath, filename, replacement, interactive)


#------------------------------------------------------------------------------------------------------------------------

def call_sp(command, **arg_list):
    #run that beast
    p = subprocess.Popen(command, shell=True, **arg_list)
    p.communicate()

#------------------------------------------------------------------------------------------------------------------------

def read_content(the_file):
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

warning_dict =      {'filepath':    "Start from home? \n('y' or anything else to re-enter)\n",
                     'filename':    "Sure you don't want to search by filename? \n('y' or anything else to re-enter)\n"}
                    

confirmation_dict = {'setting':     ["\nIs ", " the correct setting? ('y' or anything else to re-enter)\n"],
                     'filepath':    ["\nIs ", " the correct path to start from?\n('y' or anything else to re-enter)\n"],
                     'filepath_home':    ["\nIs $HOME", " the correct path to start from?\n('y' or anything else to re-enter)\n"],
                     'filename':    ["\nIs ", " the correct filename to search by? \n('y' or anything else to re-enter)\n"],
                     'filename_blank': ["Don't search by filename?\n('y' or anything else to re-enter)\n", ""],
                     'replacement': ["\nAre you sure you want to replace ", " with ", "? ('y' or 'n' to skip this file)\n"]}
                    

gathering_dict =    {'setting':     "\nWhat setting do you want to replace?\n",
                     'filepath':    "\nPath to start from? (hit enter to start from home)\n",
                     'filename':    "\nSearch by certain filename? (like 'settings.py')\n",
                     'replacement': "\nWhat do you want to substitute in?\n"}
                    
#------------------------------------------------------------------------------------------------------------------------

def gather(item):
    answer = raw_input(bcolors.OKBLUE + gathering_dict[item] + bcolors.ENDC + '\n')
    return answer

#------------------------------------------------------------------------------------------------------------------------

def confirm(answer, item):
    while True:
        confirm = raw_input(bcolors.WARNING + confirmation_dict[item][0] + answer + confirmation_dict[item][1] + bcolors.ENDC)
        if confirm == 'y':
            confirmation = True
        else:
            confirmation = False
        return confirmation

#------------------------------------------------------------------------------------------------------------------------

def confirm_replacement(item_to_replace, answer):
    while True:
        if not item_to_replace:
            the_item = "[empty string]"
        else:
            the_item = item_to_replace
        confirm = raw_input(bcolors.WARNING + confirmation_dict['replacement'][0] + the_item + confirmation_dict['replacement'][1]
                            + answer + confirmation_dict['replacement'][2] + bcolors.ENDC)
        if confirm == 'y':
            confirmation = True
            return confirmation
        elif confirm == 'n':
            confirmation = False
            return confirmation
        else:
            continue

#------------------------------------------------------------------------------------------------------------------------

def ask_for_setting(mode):
    while True:
        setting = gather('setting')
        if setting == '':
            continue
        if mode == 'safe':
            confirmation = confirm(setting, 'setting')
            if confirmation:
                return setting
            else:
                continue
        else:
           return setting

#------------------------------------------------------------------------------------------------------------------------

def ask_for_filepath(mode):
    while True:
        filepath = gather('filepath')
        if mode == 'safe':
            if filepath == '':
                confirmation = confirm(filepath, 'filepath_home')
            else:
                confirmation = confirm(filepath, 'filepath')
            if confirmation:
                return filepath
            else:
                continue
        else:
           return filepath

#------------------------------------------------------------------------------------------------------------------------

def ask_for_filename(mode):
    while True:
        filename = gather('filename')
        if mode == 'safe':
            if filename == '':
                confirmation = confirm(filename, 'filename_blank')
            else:
                confirmation = confirm(filename, 'filename')
            if confirmation:
                return filename
            else:
                continue
        else:
           return filename

#------------------------------------------------------------------------------------------------------------------------

def ask_for_replacement(mode):
    while True:
        replacement = gather('replacement')
        if replacement == '':
            continue
        else:
           return replacement

#------------------------------------------------------------------------------------------------------------------------

def interactive_gather(mode):
    setting =   ask_for_setting(mode)
    filepath =  ask_for_filepath(mode)
    filename =  ask_for_filename(mode)
    return (setting, filepath, filename)

#------------------------------------------------------------------------------------------------------------------------

def find_files(setting, filepath='', filename=None):
    # print "filepath: %s" % filepath
    # print "setting: %s" % setting
    # print "command: 'r\"grep\" -rl %s %s" % (setting, filepath)
    if filename:
        path = home_path + "/" + filepath
        # print 'is filename'
        b = subprocess.Popen([r"grep", "-rl", setting, path, "--include", filename], stdout=subprocess.PIPE)
    else:
        # print 'no filename'
        path = home_path
        b = subprocess.Popen([r"grep", "-rl", setting, path], stdout=subprocess.PIPE)
    files = b.stdout
    if not files:
        print bcolors.FAIL + "\nCouldn't find that setting in your files\n" + bcolors.ENDC
        return 0
    return files

#------------------------------------------------------------------------------------------------------------------------

def get_the_file_names(stdout):
    files = []
    for file in stdout:
        the_file = re.sub('\n', '', file)
        files.append(the_file)
    return files

#------------------------------------------------------------------------------------------------------------------------

def backup(the_file):
    if re.search('\.backup', the_file):
        return 0
    if not re.search('\.backup', the_file):
        the_file_backup = '%s%s' % (the_file, '.backup')
        subprocess.Popen([r"cp", the_file, the_file_backup])

#------------------------------------------------------------------------------------------------------------------------

def find_match(setting, the_file):
        content =   read_content(the_file)
        keywords = ['rx', ]
        regex_to_find_line =     "'" + setting + "':\s*'(?P<remainder>.*)'"
        regex_object = re.search(regex_to_find_line, content)
        if not regex_object:
            return 0
        else:
            match = regex_object.group(0)
            remainder = regex_object.group(1)
        return (match)

#------------------------------------------------------------------------------------------------------------------------

def setup_replacement(setting, match):
    regex_find_replacement = "'" + setting + "':\s*'(?P<remainder>.*)'"
    new_match =                 re.search(regex_find_replacement, match)
    string_to_replace = new_match.group('remainder')
    return string_to_replace

#------------------------------------------------------------------------------------------------------------------------

def grab_lines(match, file_text):
    regex =  "^.*\n.*\n" + match + "\n.*\n.*$"
    lines =                   re.search(regex, file_text)
    if lines:
        return lines
    regex =  "^.*\n" + match + "\n.*$"
    lines =                   re.search(regex, file_text)
    if lines:
        return lines
    else:
        return match


#------------------------------------------------------------------------------------------------------------------------
def get_new_content(string_to_replace, replacement, file):
    content =       read_content(file)
    new_content =   re.sub(string_to_replace, replacement, content)
    return new_content

#------------------------------------------------------------------------------------------------------------------------

def replace_setting(the_file, new_content, setting):
    write_content(the_file, new_content)
    print "\nnew content:\n\n"
    cmd = ('grep -B 2 -A 2 %s %s' % (setting, the_file))
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.stdout.read()
    print output
    return 1

#------------------------------------------------------------------------------------------------------------------------

def run_search_replace(mode):
    setting, filepath, filename, replacement, interactive = check_mode()
    if interactive:
        setting, filepath, filename = interactive_gather(mode)
    if not replacement:
        replacement = ask_for_replacement(mode)
    raw_files = find_files(setting, filepath, filename)
    files = get_the_file_names(raw_files)
    for the_file in files:
        backup(the_file)
        match = find_match(setting, the_file)
        if not match:
            continue
        if re.search('\.backup', the_file):
            continue
        if re.search('search_replace.py', the_file):
            continue
        print "\n" + bcolors.OKBLUE + the_file + bcolors.ENDC
        cmd = ('grep -B 2 -A 2 %s %s' % (setting, the_file))
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = p.stdout.read()
        rgx = re.compile(match)
        split = rgx.split(output)
        print "\nmatch:\n\n" + split[0] + bcolors.FAIL + ("%s" % match) + bcolors.ENDC + split[1]
        string_to_replace = setup_replacement(setting, match)
        if mode == 'safe' or mode == 'normal':
            confirmation = confirm_replacement(string_to_replace, replacement)
            if not confirmation:
                continue
        new_content = get_new_content(string_to_replace, replacement, the_file)
        replace_setting(the_file, new_content, setting)



run_search_replace(mode)


















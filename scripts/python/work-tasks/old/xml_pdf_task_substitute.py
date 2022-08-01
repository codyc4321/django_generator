#!/usr/bin/env python


"""for substituting xml code appropriately in a specific task"""

import subprocess
import sys
import re
from os.path import expanduser

home_path = expanduser("~")

print home_path

path = '/home/cchilders/scripts/python/temp_scripts/xml_temp.txt'



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#------------------------------------------------------------------------------------------------------------------------

keywords =  ['did_phys',
             'primary',
             'ch_symptoms',
             'services',
             'phys_lines',
             'h_svcs',
             'encounter',
             'secondary',
             'rx',
             'r_svcs',
             'symptoms',
             'physical']

#------------------------------------------------------------------------------------------------------------------------

confirmation_dict = {'replacement': ["\nAre you sure you want to replace ", " with ", "? ('y' or 'n' to skip this file)\n"]}

#------------------------------------------------------------------------------------------------------------------------

def call_sp(command, **arg_list):
    p = subprocess.Popen(command, shell=True, **arg_list)
    p.communicate()

#------------------------------------------------------------------------------------------------------------------------

def read_content(the_file):
    f = file(the_file, 'r')
    content = f.readlines()
    f.close()
    return content

#------------------------------------------------------------------------------------------------------------------------

def write_content(the_file, content):
    f = file(the_file, 'w')
    f.writelines(content)
    f.close

#------------------------------------------------------------------------------------------------------------------------


def confirm_replacement(item_to_replace, answer):
    while True:
        if not item_to_replace:
            the_item = "[empty string]"
        else:
            the_item = item_to_replace
        confirm = raw_input(bcolors.WARNING + confirmation_dict['replacement'][0] + bcolors.ENDC + bcolors.FAIL + the_item
                            + bcolors.ENDC + bcolors.WARNING + confirmation_dict['replacement'][1] + bcolors.ENDC
                            + bcolors.FAIL + answer + bcolors.ENDC + bcolors.WARNING + confirmation_dict['replacement'][2]
                            + bcolors.ENDC)
        if confirm == 'y':
            confirmation = True
            return confirmation
        elif confirm == 'n':
            confirmation = False
            return confirmation
        else:
            continue

#------------------------------------------------------------------------------------------------------------------------

def backup(the_file):
    if re.search('\.backup', the_file):
        return 0
    if not re.search('\.backup', the_file):
        the_file_backup = '%s%s' % (the_file, '.backup')
        subprocess.Popen([r"cp", the_file, the_file_backup])

#------------------------------------------------------------------------------------------------------------------------

def find_match(line):
        regex =     r"(?<!<span>)(?<!\|)([A-Z][a-zA-Z\s\-/&.;)(]+:)(?!</span>)"
        regex_object = re.search(regex, line)
        if not regex_object:
            return 0
        else:
            match = regex_object.group(0)
        return (match)

#------------------------------------------------------------------------------------------------------------------------

def setup_replacement(match):
    regex_find_replacement =     r"(?<!<span>)(?<!\|)([A-Z][a-zA-Z\s\-/&.;)(]+:)(?!</span>)"
    new_match =                 re.search(regex_find_replacement, match)
    string_to_replace = new_match.group()
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

def get_new_content(string_to_replace, replacement, line):
    new_content =   re.sub(string_to_replace, replacement, line)
    return new_content

#------------------------------------------------------------------------------------------------------------------------

def run_search_replace():
    content = read_content(path)
    backup(path)
    new_content = []
    for i, line in enumerate(content[:]):
        match = find_match(line)
        if not match:
            new_content.append(line)
            continue
        print "\n" + bcolors.OKBLUE + 'match' + bcolors.ENDC
        print bcolors.FAIL + line + bcolors.ENDC
        string_to_replace = match
        replacement = '<span>' + match + '</span>'
        confirmation = confirm_replacement(string_to_replace, replacement)
        if not confirmation:
            new_content.append(line)
            continue
        new_line = get_new_content(string_to_replace, replacement, line)
        new_content.append(new_line)
    write_content(path, new_content)



run_search_replace()


















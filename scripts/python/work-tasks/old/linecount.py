#!/usr/bin/env python

"""Breaking down our code by how many lines in each filetype for my boss"""

# first argument should be path to count from, as in 'home/username/projects/advantage'


import sys, subprocess, re, time, string
from os.path import exists, isfile, join, expanduser, isdir
from os import listdir

alpha = string.ascii_lowercase
alpha_up = string.ascii_uppercase

home_path       = expanduser('~')


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

def read_content(the_file):
    try:
        f = file(the_file, 'r')
        content = f.read()
        f.close()
        return content
    except IOError:
        return 0

#------------------------------------------------------------------------------------------------------------------------

def get_filetype(filename):
    filetype = re.search('.\w+$', filename).group()
    if filetype:
        return filetype
    else:
        filetype = re.search('/\w+$', filename).group()
    return filetype

#------------------------------------------------------------------------------------------------------------------------

def add_filetype_to_list(filetype, file_list):
    if not filetype in file_list:
        file_list.append(filetype)

#------------------------------------------------------------------------------------------------------------------------

def count_lines(text):
    nlinePat = re.compile(r'\n')
    nlineCounter = 0
    bl = nlinePat.split(text)
    for line in bl:
        nlineCounter += 1
    return nlineCounter

#------------------------------------------------------------------------------------------------------------------------

def count_lines_per_file_type(file_list):
    count_dict = {}
    for f in file_list:
        file_type = get_filetype(f)
        content = read_content(f)
        if not content:
            continue
        lines =  count_lines(content)
        if file_type in count_dict:
            count_dict[file_type] += lines
        else:
            count_dict[file_type] = lines
    return count_dict

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
    return total_files

#------------------------------------------------------------------------------------------------------------------------

def grab_names(text):
    p = re.compile(r"'([\W]+)(.*?)'")
    matches = re.findall(p, text)
    name_list = []
    for m in matches:
        name_list.append(m[1])
    return name_list

#------------------------------------------------------------------------------------------------------------------------

def alphabetize_entry(word, alpha_list=[], index=0):
    def insert_word(word, alpha_list, insert_index):
        alpha_list.insert(insert_index, word)
        return alpha_list

        alpha_list.insert(insert_index, word)
        return alpha_list

    if not alpha_list:
        alpha_list.append(word)
        return alpha_list

    if index > (len(alpha_list)-1):
        alpha_list.insert(index, word)
        return alpha_list

    for w in alpha_list:

        for i, letter in enumerate(word):
            if letter == '_':
                if i == 0 or i == 1:
                    alpha_list.insert(index, word)
                    return alpha_list
                alpha_list.insert(index, word)
                return alpha_list
            try:
                letter_against = w[i]
            except IndexError:
                index += 1
                break

            if letter_against == '_':
                if i == 0 or i == 1:
                    index += 1
                    break
                else:
                    alpha_list.insert(index, word)
                    return alpha_list

            while True:
                if letter == '/':
                    letter_value = 0
                    break
                try:
                    letter_value = alpha.index(letter)
                    break
                except ValueError:
                    try:
                        letter_value = alpha_up.index(letter)
                        break
                    except ValueError:
                            int_val = int(letter)
                            letter_value = int_val + 26
                            break

            while True:
                if letter_against == '/':
                    letter_against_value = 0
                    break
                try:
                    letter_against_value = alpha.index(letter_against)
                    break
                except ValueError:
                    try:
                        letter_against_value = alpha_up.index(letter_against)
                        break
                    except ValueError:
                            int_val = int(letter_against)
                            letter_against_value = int_val + 26
                            break


            if letter_value < letter_against_value:
                alpha_list.insert(index, word)
                return alpha_list

            elif letter_value > letter_against_value:
                index += 1
                break

            elif letter_value == letter_against_value:
                if i == (len(word) - 1):
                    alpha_list.insert(index, word)
                    return alpha_list
                continue
    alpha_list.insert(index, word)
    return alpha_list

#------------------------------------------------------------------------------------------------------------------------

def alphabetize_list(word_list):
    alpha_list = []
    for word in word_list:
        alpha_list = alphabetize_entry(word, alpha_list)
    return alpha_list

#------------------------------------------------------------------------------------------------------------------------

def grab_values(alpha_list, text):
    text = text[1:-1]
    final_string = ""
    for word in alpha_list:
        p = re.compile(r"'([\W^_]+){}':\s*(\d+)".format(word))
        match = re.search(p, text)
        prepend = match.group(1)
        value   = match.group(2)
        if prepend == '/':
            final_string += "'{}': {}\n".format(word, value)
        else:
            final_string += "'{}{}': {}\n".format(prepend, word, value)

    return final_string

#------------------------------------------------------------------------------------------------------------------------




if not exists(home_path + '/linecount'):
    call_sp('mkdir {}/linecount'.format(home_path))


if len(sys.argv) == 2:
    starting_dir = sys.argv[1]


if len(sys.argv) != 2:
    while True:
        the_dir = raw_input('Enter a directory name past your home path ("projects" will get you "home/user/projects"):\n')
        the_path = home_path + '/' + the_dir
        print the_path
        if not the_dir:
            continue
        break


dirs_to_check = get_only_dirs(the_path)

files = get_files_to_check(dirs_to_check)

final_count_text = count_lines_per_file_type(files)


call_sp('echo "final count: {}" > {home_path}/linecount/count.txt'.format(final_count_text, home_path=home_path))

content = read_content('{home_path}/linecount/count.txt'.format(home_path=home_path))

names = grab_names(content)
alp = alphabetize_list(names)
final_string = grab_values(alp, content)
call_sp('echo "final count:\n\n{final_string}" > {home_path}/linecount/count.txt'.format(final_string, home_path=home_path))
call_sp('cat {home_path}/linecount/count.txt'.format(home_path=home_path))

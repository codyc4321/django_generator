#!/usr/bin/env python
# coding: utf-8

import re, time

f = "/home/cchilders/scripts/python/fakecss.txt"

#------------------------------------------------------------------------------------------------------------------------

def call_sp(command, **arg_list):
    p=subprocess.Popen(command, shell=True, **arg_list)
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


special_chars = r'.$^|()[]+?*!<>'

def escape_special_chars(the_input):
    for char in the_input:
        if char in special_chars:
            the_input = the_input.replace(char, '\{}'.format(char))
    return the_input

def escape_bad_chars_in_groups(the_input):
    if type(the_input) == type(list()):
        string = ''.join(the_input)
    elif type(the_input) == type(str()):
        string = the_input
    else:
        raise Exception
    for char in string:
        if char == '[' or char == ']':
            string = string.replace(char, '\{}'.format(char))
    return string

#works
def count_indentation(l):
    if l == '\n':
        return 0
    rgx = r"^\s+"
    match = re.match(rgx, l)
    if match:
        length = len(match.group())
        return length
    else:
        return 0

#returns 4 letter word for indentation; easy to remember
def compare_indentation(current, next):
    if count_indentation(current) < count_indentation(next):
        return 'more'
    elif count_indentation(current) > count_indentation(next):
        return 'less'
    else:
        return 'same'


def ends_with(l, *chars):
    if len(chars) == 1:
        if len(chars[0]) > 1:
            rgx = "{}\s*$".format(chars[0])
        else:
            rgx = "{}\s*$".format(escape_special_chars(chars[0]))
    else:
        all_single_chars = True
        for char in chars:
            if len(char) > 1:
                all_single_chars = False
                break
        if all_single_chars:
            char_string = ''.join(chars)
            char_string = escape_bad_chars_in_groups(char_string)
            rgx = "[{}]\s*$".format(char_string)
        else:
            single_chars = []
            to_join = []
            for char in chars:
                if len(char) == 1:
                    single_chars.append(char)
                else:
                    to_join.append(char)
            if single_chars:
                to_join.append(escape_bad_chars_in_groups(single_chars))
            rgx_start = "|".join(to_join)
            rgx = "{}\s*$".format(rgx_start)

    return re.search(rgx, l)

def starts_with(l, *chars):
    if len(chars) == 1:
        if len(chars[0]) > 1:
            rgx = "^\s*{}".format(chars[0])
        else:
            rgx = "^\s*{}".format(escape_special_chars(chars[0]))
    else:
        all_single_chars = True
        for char in chars:
            if len(char) > 1:
                all_single_chars = False
                break
        if all_single_chars:
            char_string = ''.join(chars)
            char_string = escape_bad_chars_in_groups(char_string)
            rgx = "^\s*[{}]".format(char_string)
        else:
            single_chars = []
            to_join = []
            for char in chars:
                if len(char) == 1:
                    single_chars.append(char)
                else:
                    to_join.append(char)
            if single_chars:
                to_join.append('[' + escape_bad_chars_in_groups(single_chars) + ']')
            rgx_start = "|".join(to_join)
            rgx = "^\s*{}".format(rgx_start)
    return re.match(rgx, l)

def ensure_ends_with_newline(line_list):
    for i, line in enumerate(line_list):
        if not ends_with(line, '\n'):
            line_list[i] = add_to_end('', line)
    return line_list

def attribute_bool(l):
    rgx = '^\s*.*:\s*.*$'
    return re.match(rgx, l)

def mixin_bool(l):
    rgx_sass = '^\s\+'
    return re.match(rgx_sass, l)

def add_to_end(char, l):
    if l[-1] != '\n':
        line_text = l + char + '\n'
    else:
        line_text = l[:-1]
        line_text += '{}\n'.format(char)
    return line_text


def check_for_end_of_file(line_list, i):
    remainder_of_list = line_list[(i+1):]
    for line in remainder_of_list:
        if line != '\n':
            return False
    return True

def process_end_of_file(line_list, i):
    end = len(line_list)
    line_list.insert(end, '}\n')
    return line_list


def check_for_multiline_opening_statement(line_list, i):
    if line_list[i] in ['\n', '}', '{']:
        return False
    current_line = line_list[i]
    curr_inden = count_indentation(current_line)
    if count_indentation(line_list[i+1]) == 0 and curr_inden == 0:
        return True
    return False

def check_for_opening_statement(line_list, i):
    if line_list[i] in ['\n', '}', '{']:
        return False
    current_line = line_list[i]
    remainder_of_list = line_list[(i+1):]
    curr_inden = count_indentation(current_line)
    for line in remainder_of_list:
        if line == '\n':
            pass
        elif count_indentation(line) < curr_inden:
            return False
        elif count_indentation(line) > curr_inden:
            return True
        elif count_indentation(line) == curr_inden:
            return False


def check_for_closing_statement(line_list, i):
    """

    type : bool
    """
    current_line = line_list[i]
    remainder_of_list = line_list[(i+1):]
    curr_inden = count_indentation(current_line)
    for line in remainder_of_list:
        if line == '\n':
            pass
        elif count_indentation(line) == curr_inden:
            return False
        elif count_indentation(line) < curr_inden:
            return True
    return True


def check_for_import(line_list, i):
    rgx = "^@import\s+(?P<file>[A-Za-z0-9-_]+)"
    return re.match(rgx, line_list[i])


def check_for_mixin_usage(line_list, i):
    rgx = "^\s*\+.*?[)]"
    return re.match(rgx, line_list[i])

def check_for_mixin_declaration(line_list, i):
    line = line_list[i]
    if count_indentation(line) == 0:
        rgx = "^="
        return re.match(rgx, line_list[i])
    else:
        return False

def process_opening_statement(line_list, i):
    line_list[i] = add_to_end('{', line_list[i])
    return line_list


def process_center_statement(line_list, i):
    line_list[i] = add_to_end(';', line_list[i])
    return line_list


def process_closing_statement(line_list, i):
    next_line_index = i + 1
    try:
        next_line = line_list[next_line_index]
    except IndexError:
        return line_list.append('}\n'), 40
    curr_line = line_list[i]
    if not ends_with(curr_line, ';'):
        line_list[i] = add_to_end(';', curr_line)
    if line_list[next_line_index] != '\n':
        line_list.insert(next_line_index, '}')
        line_list.insert(next_line_index+1, '\n')
        increment = 3
    else:
        line_list = add_to_end('}', line_list[i])
        increment = 2
    return line_list, increment


def process_import(line_list, i):
    rgx = "^@import\s+(?P<contents>.*)$"
    match = re.match(rgx, line_list[i])
    if not match:
        return Exception, "nothing to process"
    contents = match.group('contents')
    sub_str = "'" + contents + "';"
    new = re.sub(contents, sub_str, line_list[i])
    line_list[i] = new
    return line_list


def process_mixin_usage(line_list, i):
    rgx = "^\s*(?P<contents>\+.*?[)])"
    match = re.match(rgx, line_list[i])
    if not match:
        return Exception, "nothing to process"
    contents = match.group('contents')
    sub_str = "@include " + contents + ";"
    rgx = escape_special_chars(contents)
    new = re.sub(rgx, sub_str, line_list[i])
    # time.sleep(5)
    line_list[i] = new
    return line_list

def process_mixin_declaration(line_list, i):
    rgx = "^\=(?P<contents>\+.*?[)])"
    match = re.match(rgx, line_list[i])
    if not match:
        return Exception, "nothing to process"
    contents = match.group('contents')
    sub_str = "@mixin " + contents + " {"
    rgx = escape_special_chars(contents)
    # print rgx
    new = re.sub(rgx, sub_str, line_list[i])
    # time.sleep(5)
    line_list[i] = new
    return line_list


def categorize_line(line_list, i):
    line = line_list[i]
    if line == '\n':
        return 'new_line'
    if check_for_mixin_usage(line_list, i):
        return 'mixin_usage'
    if check_for_import(line_list, i):
        return 'import'
    if check_for_multiline_opening_statement(line_list, i):
        return 'multiline_open_statement'
    if check_for_opening_statement(line_list, i):
        return 'open_statement'
    return 'attribute'

def process_line(content, i):
    def handle_closing(line_list, i):
        boolean = check_for_closing_statement(line_list, i)
        if boolean:
            close = process_closing_statement(line_list, i)
            return line_list, close[1]
        else:
            return line_list, 1

    line = content[i]
    end = len(content) - 1
    if i == end:
        if line == '\n':
            content.append('}')
            return content, 40
        else:
            handle_line(content, i)
            return content, 40
    else:
        return handle_line(content, i)
    type = categorize_line(content, i)

    if i == end:
        if line == '\n':
            content.append('}')
            return content, 40
        else:
            handle_line(content, i)
            return content, 40
    else:
        return handle_line(content, i)

    if line == '\n':
        return content, 1
    if line == '}\n':
        return content, 1
    if type == 'mixin_usage':
        process_mixin_usage(line_list, i)
        return handle_closing(line_list, i)
    if type == 'import':
        process_import(line_list, i)
        return handle_closing(line_list, i)
    if type == 'multiline_open_statement':
        return content, 1
    if type == 'open_statement':
        process_opening_statement(line_list, i)
        return content, 1
    if type == 'attribute':
        process_center_statement(line_list, i)
        return content, 1



def process_file(content):
    end = len(content) - 1
    i = 0
    # lines = None
    while True:
        if i > len(content):
            break
        content, tally = process_line(content, i)
        # time.sleep(15)
        i += tally
    ensure_ends_with_newline(content)
    return content




def run_it():
    content_as_lines = read_content(f)
    new_lines = process_file(content_as_lines)
    write_content(f, new_lines)

run_it()

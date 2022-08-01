#!/usr/bin/env python

import os, sys, re, optparse, time, subprocess

homepath = os.getenv("HOME")

"""my take on Atom 'beautify', allows me to blast thousands of lines of code a day like a madman
and format it pretty at the end of the day the way I like"""

def replace_if_greater(incumbent, possible_replacement):
    if possible_replacement > incumbent:
        incumbent = possible_replacement
    return incumbent
        
#----------------------------------------------------------------------------------------------------

def read_lines(the_file):
    f = file(the_file, 'r')
    content = f.readlines()
    f.close()
    return content

#------------------------------------------------------------------------------------------------------------------------

def read_content(the_file):
    f = file(the_file, 'r')
    content = f.read()
    f.close()
    return content

#------------------------------------------------------------------------------------------------------------------------

def write_lines(the_file, lines):
    f = file(the_file, 'w')
    f.writelines(lines)
    f.close

#------------------------------------------------------------------------------------------------------------------------

def write_content(the_file, content):
    f = file(the_file, 'w')
    f.write(content)
    f.close

#------------------------------------------------------------------------------------------------------------------------

def append_lines(the_file, lines):
    f = file(the_file, 'a')
    f.writelines(lines)
    f.close

#------------------------------------------------------------------------------------------------------------------------

def append_content(the_file, content):
    f = file(the_file, 'a')
    f.write(content)
    f.close

#-------------------------------------------------------------------------------------------------------------------------

def clear_content(the_file):
    f = file(the_filreplace_if_greatere, 'w')
    f.write('')
    f.close

#-------------------------------------------------------------------------------------------------------------------------

def clear_folder(dirpath):
    for root, dirs, files in os.walk(dirpath):
        for f in files:
            fullpath = os.path.join(root, f)
            clear_content(fullpath)

#----------------------------------------------------------------------------------------------------

def backup(the_file):
    if re.search('\.backup', the_file):
        return 0
    else:
        the_file_backup = '%s%s' % (the_file, '.backup')
        subprocess.Popen([r"cp", the_file, the_file_backup])
        
#-------------------------------------------------------------------------------------------------------------------------

def count_indentation(l):
    if l == '\n':
        return 0
    rgx = r"^\s+"
    match = re.search(rgx, l)
    if match:
        length = len(match.group())
        return length

#-------------------------------------------------------------------------------------------------------------------------

def check_if_variable_declaration(line):
    rgx = r"^\s*[a-zA-Z0-9_-]+\s*(?=[=])"
    return re.search(rgx, line)

#----------------------------------------------------------------------------------------------------

def get_min_spacing_for_line_group(lines):
    rgx = r"^(?P<size>\s*[#]?[a-zA-Z\._-]+)\s*[=]"
    longest = 0
    longest_line = ""
    for i, line in enumerate(lines):
        try:
            size = re.search(rgx, line).group('size')
            l = len(size)
            if l > longest:
                longest = l
                longest_line = line
        except AttributeError:
            pass
    #correcget_max_spacing_for_line_groupurn min_length
    else:
        mod = longest % 4
        space_to_go = 4 - mod
        min_length = longest + space_to_go
        return min_length

#----------------------------------------------------------------------------------------------------

def reprocess_line(line, min_length):
    assert min_length % 4 == 0, "the length you're setting lines to isn't divisble by 4"
    var_rgx = r"^(?P<var>\s*[#]?[a-zA-Z0-9\._-]+)\s*[=]\s*(?P<remainder>.*)$"
    # comment_rgx = r"^(?P<var>\s*[a-zA-Z0-9\._-]+)\s*[=]\s*(?P<remainder>.*)$"
    match = re.search(var_rgx, line)
    if not match:
        return line
    var = match.group('var')
    remainder = match.group('remainder')
    var_length = len(var)
    spaces_needed =  min_length - var_length
    spaces = " " * spaces_needed
    new_line = var + spaces + "= " + remainder
    return new_line

#----------------------------------------------------------------------------------------------------

def get_line_groups_indexes(file_lines):
    def _add_info_dict(start=None, end=None, indentation=None):
        dict_addition = {'start': start, 'end': end, 'indentation': indentation}
        return dict_addition
    def _reset():
        within_current_group, current_start, indentation = False, None, None
    def _none_to_zero(item):
        if not item:
            return 0
        return item
        
    info_dicts = []
    
    within_current_group = False
    current_start = None
    indentation = None
    gap         = 0
    
    for i, line in enumerate(file_lines):
        new_line_rgx = r"^\n$"
        comment_rgx = r"^\s*[#]"
        # file lines start at 0 here, cuz enumerate always is 0

        if line == '\n':
            gap += 1
        # if within_current_group:
        #     if current_start:
        #         if not (i - current_start) > 5:
        #             if re.search(new_line_rgx, line) or re.search(comment_rgx, line):
        #                 print 'we reached continue'
        #                 continue
        if not within_current_group:
            if check_if_variable_declaration(line):
                indentation = count_indentation(line)
                current_start = i
                within_current_group = True
            else:
                continue
        elif within_current_group:
            if check_if_variable_declaration(line):
                gap = 0
                if count_indentation(line) != indentation:
                    info_dicts.append(_add_info_dict(start=current_start, end=i, indentation=indentation))
                    within_current_group, current_start, indentation, gap = True, i, count_indentation(line), 0
                    continue                
            else:
                if re.search(new_line_rgx, line) or re.search(comment_rgx, line):
                    if gap < 5:
                        continue
                    else:
                        info_dicts.append(_add_info_dict(start=current_start, end=i, indentation=indentation))
                        within_current_group, current_start, indentation, gap = False, None, None, 0
    else:
        info_dicts.append(_add_info_dict(start=current_start, end=len(file_lines), indentation=indentation))
        
        
    for d in info_dicts:
        min_length = get_min_spacing_for_line_group(lines[d['start']:d['end']])
        d['min_length'] = min_length
    return info_dicts

#----------------------------------------------------------------------------------------------------

# def add_min_spacing_to_each_info_dict(lines, information_dicts):
#     for d in information_dicts:
#         temp_lines = lines[d['start']]
    
    
def reprocess_each_line(lines, information_dicts):
    starting_points = []
    ending_points = []
    min_length_dict = {}
    for d in information_dicts:
        starting_points.append(d['start'])
        ending_points.append(d['end'])

        min_length_dict[d['start']] = d['min_length']

    new_file_lines = []
    
    within_current_group = False
    current_min_length = None
    
    for i, line in enumerate(lines):
        # time.sleep(3)
        if not within_current_group:
            if i in starting_points:
                within_current_group = True
                current_min_length = min_length_dict[i]
                new_file_lines.append(reprocess_line(line, current_min_length))
            else:
                new_file_lines.append(line)
        else:
            if i in ending_points:
                if i in starting_points:
                    current_min_length = min_length_dict[i]
                    new_file_lines.append(reprocess_line(line, current_min_length))
                # if i is the end, and not start of a new group
                else:
                    within_current_group = False
                    current_min_length = None
                    new_file_lines.append(line)
            else:
                new_file_lines.append(reprocess_line(line, current_min_length))
    for i, line in enumerate(new_file_lines):
        if not line.endswith('\n'):
            new_file_lines[i] = line + '\n'
    return "".join(new_file_lines)



#----------------------------------------------------------------------------------------------------


filepath = sys.argv[1]
# backup(filepath)
lines = read_lines(filepath)
info = get_line_groups_indexes(lines)
new_file_lines = reprocess_each_line(lines, info)
write_lines(filepath, new_file_lines)
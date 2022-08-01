#!/usr/bin/env python

"""get all Django models from a single file. returns the actual full text of the model, from start to finish, doesn't return model names yet"""

def count_indentation(l):
    if l == '\n':
        return 0
    rgx = r"^\s+"
    match = re.match(rgx, l)
    if match:
        length = len(match.group()
        return length
    else:
        return 0

#------------------------------------------------------------------------------------------------------------------------

def check_model_start(line):
    regex = r"^class\s+\w+\(models.Model"
    return re.search(regex, line)

#------------------------------------------------------------------------------------------------------------------------

def get_model_name_or_None(line):
    regex = r"^class\s+(\w+)\(models.Model"
    try:
        match = re.search(regex, line)
        return match.group(1)
    except:
        return None

#------------------------------------------------------------------------------------------------------------------------

def check_model_end(line):
    if not re.search(r"^#", line):
        if count_indentation(line) == 0:
            return True
    return False

#------------------------------------------------------------------------------------------------------------------------


def get_models_from_file(file):

    lines     = read_file_lines(file)
    currently_within_model  = False
    start_stop_tuples       = []
    current_start           = None

    for i, line in enumerate(lines):
        if currently_within_model:
            if line == '\n':
                continue
            if check_model_end(line):
                start_stop_tuples.append((current_start, i))
                currently_within_model  = False
                current_start           = None
        else:
            if check_model_start(line):
                current_start           = i
                currently_within_model  = True

    models = []

    for tup in start_stop_tuples:
        print "tup: ", tup
        model_lines = lines[tup[0]:tup[1]]
        this_model  = "\n".join(model_lines)
        models.append(this_model)

    return models

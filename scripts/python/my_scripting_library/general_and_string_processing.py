import re 

from .decorators import do_for_each_in_list


#-------------------------------------------------------------------------------------------------

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
        
#----------------------------------------------------------------------------------------------------

def andify_list(the_list):
    def _string_clean(l):
        clean_list = []
        for item in l:
            clean_list.append(str(item))
        return clean_list
        
    the_list = _string_clean(the_list)
    if len(the_list) == 0:
        return ""
    if len(the_list) == 1:
        return the_list[0] 
    if len(the_list) == 2:
        return the_list[0] + ' and ' + the_list[1]
    head = the_list[:-1]
    head_string = ", ".join(head)
    return head_string + " and " + the_list[-1]

#----------------------------------------------------------------------------------------------------

def list_to_string(mystery_item):
    if type(mystery_item) == str:
        return mystery_item
    string = ""
    for thing in mystery_item:
        if thing.endswith('\n'):   
            string += thing
        else:
            string += thing + '\n'
    return string
    
#----------------------------------------------------------------------------------------------------

def choices_to_list(the_string):
    return re.findall(r"(\w+)", the_string)
    
#----------------------------------------------------------------------------------------------------

@do_for_each_in_list
def ensure_endswith(item, ender):
    if item.endswith(ender):
        return item
    else:
        return item + ender
        
#----------------------------------------------------------------------------------------------------

@do_for_each_in_list
def ensure_startswith(item, starter):
    if item.startswith(starter):
        return item
    else:
        return starter + item

import os 

from .general_and_string_processing import andify_list


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    
#----------------------------------------------------------------------------------------------------

def gather(msg=None, default=None):
    while True:
        text = bcolors.OKBLUE + msg + bcolors.ENDC + '\n'
        if default:
            text += "the default is {default}...press enter to accept\n".format(default=default)
            answer = raw_input(text)
            return answer or default
        answer = raw_input(text)
        if not answer:
            continue
        return answer

#----------------------------------------------------------------------------------------------------

def confirm(msg=None):
    answer = raw_input(bcolors.OKBLUE + msg + " ('y' or anything else to restart)" + bcolors.ENDC + '\n')
    if answer == 'y':
        return True      
    else:
        False 
    
#----------------------------------------------------------------------------------------------------

def gather_and_confirm(msg=None, confirm_message=None):
    while True:
        answer = raw_input(bcolors.OKBLUE + msg + bcolors.ENDC + '\n')
        confirmation = confirm(msg=confirm_message)
        if confirmation:
            return answer      
        else:
            continue 
    
#----------------------------------------------------------------------------------------------------

def gather_boolean(msg=None):
    while True:
        answer = raw_input(bcolors.OKBLUE + msg + bcolors.ENDC + '\n')
        if answer == 'y':
            return True      
        elif answer == 'n':
            return False
        continue 
        
#----------------------------------------------------------------------------------------------------

def pick_items_from_list(item_list):
    names_string = andify_list(item_list)
    
    def _get_int_list(number_string):
        list_of_numberstrings = number_string.split(',')
        int_list = []
        for number in list_of_numberstrings:
            int_list.append(int(number))
        return int_list
    
    def _split_answer_list(answer_string):
            new_list = answer_string.split(',')
            return new_list 
    
    def _pick_by_number(int_list, this_item_list):
        picked_items = []
        for i in int_list:
            picked_items.append(this_item_list[(i-1)])
        return picked_items
        
    def _prompt(answer=None):
        if answer == None:
            answer = gather("Pick from {names_string}...if you want more than 1, separate like \"substring1, substring2\"".format(names_string=names_string))
            try:
                int_list = _get_int_list(answer)
                picked_items = _pick_by_number(int_list, item_list)
                return picked_items
            except:
                try:
                    answer_list = _split_answer_list(answer)
                    picked_items = check_for_answer_matches(item_list, answer_list)
                    return picked_items
                except:
                    return _prompt(answer=answer)
        try:
            int_list = _get_int_list(answer)
            picked_class_names = _pick_by_number(int_list, item_list)
            return picked_class_names
        except:
            pass
        matches = check_for_answer_matches(item_list, answer)
        matches_string = andify_list(matches)
        
        if len(matches) == 0:
            answer = gather("That string didn't match any of {names_string}, please try again".format(names_string=names_string))
            _prompt(answer=answer)
        elif len(matches) == 1:
            answer = gather("Is {matches_string} OK? ('y' or 'n' to restart)".format(matches_string=matches_string))
            if answer == 'y':
                return matches
            elif answer == 'n':
                return _prompt()
            return matches
        elif len(matches) > 1:
            answer = gather("That string matched {matches_string}, is that OK? ('y' or 'n' to restart)".format(matches_string=matches_string))
            if answer == 'y':
                return matches
            elif answer == 'n':
                return _prompt()

    return _prompt()

#----------------------------------------------------------------------------------------------------

def pick_template_file(project_path=None, app_name=None, default=None):
    templates_path_for_app = os.path.join(project_path, "templates", app_name)
    for root, dirs, files in os.walk(templates_path_for_app):
        template_files = files
        template_files_string = andify_list(files)
        dirs[:]=[]
    while True:
        text = "You have {template_files_string} available...do you want to enter a new file?\n('n' or enter a new template name)\n"\
               .format(template_files_string=template_files_string)
        if default:
            text += "the default is {default}...press enter to accept\n".format(default=default)
        answer = gather(text)
        if not answer:
            if default:
                return default
            else:
                continue
        if answer == 'n':
            answer = pick_items_from_list(template_files)
        return answer
        
#----------------------------------------------------------------------------------------------------

def check_for_answer_matches(the_list, answers):
    if type(answers) != list:
        answers = [answers]
    matches = []
    the_list.sort()
    for answer in answers:
        for item in the_list:
            lowercase_item = item.lower()
            try:
                rgx = r"^{answer}".format(answer=answer)
                match = re.search(rgx, lowercase_item).group()
                matches.append(item)
                the_list.remove(item)
                break
            except:
                item_set = set(lowercase_item)
                answer_set = set(answer)
                if answer_set.issubset(item_set):
                    matches.append(item)
                    break
    return matches
    
    
    
    
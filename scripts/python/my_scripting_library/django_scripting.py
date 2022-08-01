import os, re, time, sys

from django.template.defaultfilters import slugify

from .sysadmin import read_lines, read_content, write_content
from .interactive import pick_items_from_list, confirm
from .general_and_string_processing import count_indentation

#----------------------------------------------------------------------------------------------------

def get_templates_path(project_path):
    fullpath = os.path.join(project_path, "templates")
    return fullpath

#----------------------------------------------------------------------------------------------------

def get_path_for_django_file(project_path=None, app_name=None, filename=None):
    if not filename.endswith('.py'):
        filename = filename + '.py'
    full_path = os.path.join(project_path, app_name, filename)
    return full_path
    
#----------------------------------------------------------------------------------------------------

def append_django_content(project_path=None, app_name=None, filename=None, content=None):
    if not filename.endswith('.py'):
        filename = filename + '.py'
    full_path = os.path.join(project_path, app_name, filename)
    append_content(full_path, content)
    
#----------------------------------------------------------------------------------------------------

def write_django_content(project_path=None, app_name=None, filename=None, content=None):
    if not filename.endswith('.py'):
        filename = filename + '.py'
    full_path = os.path.join(project_path, app_name, filename)
    write_content(full_path, content)
    
#----------------------------------------------------------------------------------------------------
def check_if_root_directory(project_path):
    for root, dirs, files in os.walk(project_path):
        if "manage.py" in files:
            print 'found manage.py...'
        else:
            confirmation = confirm(msg="You aren't in the main project directory..is that OK?")
            if confirmation:
                dirs[:]=[]
            else:
                sys.exit()
        dirs[:]=[]
                
#------------------------------------------------------------------------------------------------------------------------

def check_class_start(line):
    regex = r"^class\s+\w+\("
    return re.search(regex, line)

#----------------------------------------------------------------------------------------------------------------

def check_class_end(line):
    if not re.search(r"^\s*#", line):
        if count_indentation(line) == 0:
            return True
    return False

#---------------------------------------------------------------------------------

def get_class_name_or_None(line):
    regex = r"^class\s+(\w+)\("
    try:
        match = re.search(regex, line)
        return match.group(1)
    except:
        return None

#------------------------------------------------------------------------------------------------------------------------

def get_classes_info_from_file(file):
    """ returns a list of dicts
    [{'name': 'Article', 
      'start_to_stop': (23, 26), 
      'class_text': 'class Article(models.Model):\n
                       title = models.CharField()\n
                       url   = models.UrlField\n'
      'filepath': '/thefilepath/'}]
    """
    lines = read_lines(file)

    currently_within_class  = False
    current_start           = None
    class_name              = None
    single_class_dict       = {}
    class_dicts             = []

    for i, line in enumerate(lines):

        temp_class_name = get_class_name_or_None(line)
        
        if currently_within_class:
            if line == '\n':
                continue
                
            elif temp_class_name:
                class_dicts.append({'name': class_name, 'start_to_stop': (current_start, (i-1),)})
                currently_within_class              = True
                current_start                       = i
                class_name                          = temp_class_name
                continue
                
            elif check_class_end(line):
                class_dicts.append({'name': class_name, 'start_to_stop': (current_start, (i-1),)})
                time.sleep(8)
                currently_within_class              = False
                current_start                       = None
                continue
        else:
            if temp_class_name:
                current_start                       = i
                currently_within_class              = True
                class_name                          = temp_class_name
                continue
    else:
        if currently_within_class:
            class_dicts.append({'name': class_name, 'start_to_stop': (current_start, len(lines),)})

    for c_dict in class_dicts:
        class_text = lines[c_dict['start_to_stop'][0]:c_dict['start_to_stop'][1]]
        this_class  = "".join(class_text)
        c_dict['class_text'] = this_class
        c_dict['filepath'] = file
    return class_dicts

#----------------------------------------------------------------------------------------------------

def get_values_from_dicts_by_key(dicts, key):
    values = []
    for d in dicts:
        values.append(d[key])
    return values
    
    
#----------------------------------------------------------------------------------------------------    

def get_all_models(project_path):
    check_if_root_directory(project_path)
            
    models = []
    for root, dirs, files in os.walk(project_path):
        for f in files:
            if f == 'models.py':
                fullpath = os.path.join(root, f)
                info_dicts = get_classes_info_from_file(fullpath)
                for d in info_dicts:
                    models.append(d)
        for d in dirs:
            if d == 'models':
                dirpath = os.path.join(root, d)
                for subroot, subdirs, subfiles in os.walk(dirpath):
                    for subf in subfiles:
                        subfullpath = os.path.join(subroot, subf)
                        info_dicts = get_classes_info_from_file(fullpath)
                        for d in info_dicts:
                            models.append(d)
    return models

#----------------------------------------------------------------------------------------------------

def list_models_from_info_dicts(dicts):
    model_names = []
    for this_dict in dicts:
        model_names.append(this_dict['name'])
    return model_names
    
#----------------------------------------------------------------------------------------------------

def get_all_fields_from_model(model_text):
    field_rgx = r"^[ ]{4}(?P<field_name>\w+)\s*[=]"
    fields = re.findall(field_rgx, model_text, re.MULTILINE)
    return fields
    
#----------------------------------------------------------------------------------------------------

def get_settings_path(starting_dir):
    for (dirpath, dirnames, filenames) in os.walk(starting_dir):
        if 'settings.py' in filenames:
            settings_path = dirpath + '/settings.py'
            break
    try:
        return settings_path
    except:
        raise Exception("you need to call this script from the manage.py level of the project")
    
#----------------------------------------------------------------------------------------------------

def get_installed_apps(project_path):
    settings_path       = get_settings_path(project_path)
    rgx                 = "INSTALLED_APPS.*?(?=\))"
    settings_content    = read_content(settings_path)
    match               = re.search(rgx, settings_content, re.DOTALL)
    installed_apps_text = match.group()
    installed_apps      = re.findall(r"['\"](?P<app_name>[\w.]+)['\"]", installed_apps_text)
    return installed_apps
    
#----------------------------------------------------------------------------------------------------

def get_folders_from_main_dir(project_path):
    folders = []
    for root, dirs, files in os.walk(project_path):
        for d in dirs:
            dirname = d.replace((project_path+'/'), '')
            folders.append(dirname)
        dirs[:]=[]
    return folders

#----------------------------------------------------------------------------------------------------

def get_apps(project_path):
    installed_apps  = get_installed_apps(project_path)
    folders         = get_folders_from_main_dir(project_path)
    apps = []
    for folder in folders:
        if folder in installed_apps:
            apps.append(folder)
    return apps

#----------------------------------------------------------------------------------------------------

def get_folder_directly_under_other_folder(lower_folder_path, higher_folder_path):
    relative_dir = lower_folder_path.replace((higher_folder_path+'/'), '').replace(higher_folder_path, '')
    folders = []
    while 1:
        relative_dir, folder = os.path.split(relative_dir)
        if folder != "":
            folders.append(folder)
        else:
            if relative_dir != "":
                folders.append(relative_dir)
            break
    folders.reverse()
    return folders[0]
            
#----------------------------------------------------------------------------------------------------

def get_desired_models_info(project_path):
    info_dicts = get_all_models(project_path)
    modelnames = list_models_from_info_dicts(info_dicts)
    modelnames.sort()
    desired_models = pick_items_from_list(modelnames)
    # print "desired_models: ", desired_models 
    desired_dicts = []
    for info_dict in info_dicts:
        for name in desired_models:
            if name == info_dict['name']:
                desired_dicts.append(info_dict)
    return desired_dicts


#----------------------------------------------------------------------------------------------------

def insert_import_statement(filepath, import_statements):
    index = 1
    rgx = r"^from|import"
    lines = read_lines(filepath)
    for i, line in enumerate(lines):
        real_i = i + 1
        if re.search(rgx, line):
            index = real_i
    
    if type(import_statements) == str:
        import_statements = import_statements.split('\n')
    head = lines[:index]
    tail = lines[index:]
    for statement in import_statements:
        if not statement.endswith('\n'):
            statement = statement + '\n'
        if not statement in lines:
            head.append(statement)
    for line in tail:
        head.append(line)
    write_lines(filepath, head)
    
#----------------------------------------------------------------------------------------------------

def install_app_string(project_path, apps_to_install):
    """only installs apps if they aren't already there :) """
    def _format_apps_to_install(app_list, currently_installed_apps):
        string = ""
        for app in app_list:
            if app not in currently_installed_apps:
                string += "    '" + app + "',\n"
        return string

    def _check_rgx_and_rewrite(rgx):
        match = re.search(rgx, settings_content, re.DOTALL)
        if match:
            start_string    = match.group()
            new_string      = start_string + _format_apps_to_install(apps_to_install, currently_installed_apps)
            strings_list    = new_string.split("\n")
            for line in strings_list:
                if re.match(r"\s*\n\s*", line):
                    strings_list.remove(line)
            new_string              = "\n".join(strings_list)
            text                    = re.sub(rgx, new_string, settings_content, flags=re.DOTALL)
            write_content(settings_path, text)
            return True
        else:
            return False
            
    check_if_root_directory(project_path)
    settings_path           = get_settings_path(project_path)
    settings_content        = read_content(settings_path)
    currently_installed_apps= get_installed_apps(project_path)
    list_rgx                = r"INSTALLED_APPS\s*[=]\s*[\[].*?(?=])"
    tuple_rgx               = r"INSTALLED_APPS\s*[=]\s*[(].*?(?=\))"
    if _check_rgx_and_rewrite(list_rgx):
        return 1
    elif _check_rgx_and_rewrite(tuple_rgx):
        return 1
    else:
        raise Exception("Do you not have a settings.py in this project?")
        
    


    
#----------------------------------------------------------------------------------------------------

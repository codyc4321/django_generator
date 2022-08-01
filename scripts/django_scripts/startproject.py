#!/usr/bin/env python

"""setup basic project, configured with templates dir and whatnot"""


from my_scripting_library import *

ACCOUNT_APP_PATH = "/home/cchilders/scripts/apps_repo/accounts"


#-------------------------------------------------------------------------------------------------------------------------

def rewrite_content(filepath, to_replace, replacement):

    def _read_file(filepath):
        f = file(filepath, 'r')
        content = f.read()
        return content

    content = _read_file(filepath)
    text    = re.sub(to_replace, replacement, content)
    write_file(filepath, text)

#-------------------------------------------------------------------------------------------------------------------------

def set_app_dirs_to_false(settings_path):
    content = settings_path
    rgx = "'APP_DIRS'\s*:\s*True"
    new_match =                 re.search(regex_find_replacement, match)
    string_to_replace = new_match.group()
    new_content = re.sub(rgx, "'APP_DIRS': False", content)
    return string_to_replace



current_dir=os.getcwd()
project_name = sys.argv[1]
project_path = os.path.join(current_dir, project_name)
print "project path: ", project_path
call_sp('django-admin.py startproject {}'.format(project_name), **{'cwd': current_dir})
time.sleep(2)

settings_path = get_settings_path(project_path)
settings_content = read_content(settings_path)
print 'settings', settings_path
#comment out session middleware causing problems
# rewrite_content(settings_path, "'django.contrib.auth.middleware.SessionAuthenticationMiddleware',", "# 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',")


#make templates folder
#why isnt this working on windows?
# template_dir = os.path.join(project_path + 'templates')
template_dir = project_path + '\\templates'
print template_dir
if not os.path.isdir(template_dir):
    os.makedirs(template_dir)


payload = \
"""TEMPLATES = [\n
    {\n
        'BACKEND': 'django.template.backends.django.DjangoTemplates',\n
        'APP_DIRS': False,\n
        'DIRS' = [os.path.join(BASE_DIR, \"templates\")],\n
    },\n
]\n
\n
"""

append_to_file(settings_path, payload)
print ACCOUNT_APP_PATH
print project_path
call_sp("cp -r {account_app} {project_path}".format(account_app=ACCOUNT_APP_PATH, project_path=project_path))

rgx = "INSTALLED_APPS.*?(?=\))"
match = re.search(rgx, settings_content, re.DOTALL)
start_string = match.group()
new_string = start_string + "    'accounts',\n"
text = re.sub(rgx, new_string, settings_content, flags=re.DOTALL)
write_content(settings_path, text)

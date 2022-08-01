#!/usr/bin/env python

"""makes all views for a file @login_required, except for accounts app (duh)"""


from my_scripting_library import *


#----------------------------------------------------------------------------------------------------

def get_views_indexes(content):
    lines = content.split("\n")
    rgx = r"def\s+\w+[(].*request.*[)]"
    line_numbers = []
    for i, line in enumerate(lines):
        if re.search(rgx, line):
            line_numbers.append(i)
    return line_numbers

#----------------------------------------------------------------------------------------------------
    
def add_login_requireds(content, indexes):
    length = len(indexes) - 1
    lines = content.split('\n')
    new_content_lines = []
    for i, index in enumerate(indexes):
        print new_content_lines
        # time.sleep(7)
        if i == 0:
            new_content_lines = new_content_lines + lines[0:indexes[i]]
            print new_content_lines
            # time.sleep(7)
            new_content_lines.append("@login_required")
            continue
        new_content_lines = new_content_lines + lines[indexes[i-1]:indexes[i]]
        new_content_lines.append("@login_required")
    new_content_lines = new_content_lines + lines[indexes[length]:]
    # ready_to_join_lines = [val for sublist in new_content_lines for val in sublist]
    return "\n".join(new_content_lines)
    
#----------------------------------------------------------------------------------------------------

apps = get_apps(CWD)

answer = gather(msg="Do you want to exclude any apps besides 'accounts'?", default="accounts")
if answer != 'accounts':
    excluded_apps = choices_to_list(answer)
    excluded_apps.append('accounts')
else:
    excluded_apps = ['accounts']

print excluded_apps
for excluded_app in excluded_apps:
    print excluded_app
    apps.remove(excluded_app)
    
for app in apps:
    view_path = get_path_for_django_file(project_path=CWD, app_name=app, filename='views')
    content = read_content(view_path)
    indexes = get_views_indexes(content)
    new_content = add_login_requireds(content, indexes)
    write_content(view_path, new_content)
    
    
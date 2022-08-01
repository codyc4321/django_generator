#!/usr/bin/env python

from my_scripting_library import *


def get_url_names(app_name, urls_content):
    rgx = r"""name[=]['"](?P<name>[\w-]+)['"]"""
    names = re.findall(rgx, urls_content)
    return names

#----------------------------------------------------------------------------------------------------

def make_links_from_names(app_name, name_list, dropdown=False):
    string = ""
    if dropdown:
        dropdown_text = " class=\"dropdown-header\""
    else:
        dropdown_text = ""
    for name in name_list:
        string += """<li{dropdown}><a href="{{% url '{app_name}:{name}' %}}">TITLEHERE</a></li>\n\n""".format(app_name=app_name, name=name, dropdown=dropdown_text)
    return string

#----------------------------------------------------------------------------------------------------

while True:
    app_name = gather(msg="Enter the app name you want to make links for:")
    filepath = get_path_for_django_file(project_path=CWD, app_name=app_name, filename='urls')
    if not filepath:
        print 'Please enter a correct app name'
        continue
    break

dropdown    = gather_boolean(msg="Do you want these as dropdown links?")
content     = read_content(filepath)
names       = get_url_names(app_name, content)
links       = make_links_from_names(app_name, names, dropdown)
print '\n'
print links

#!/usr/bin/env python

"""register app name(s) in settings.py by command line, takes a list too"""



from my_scripting_library import *

apps_to_install = sys.argv[1:]

install_app_string(CWD, apps_to_install)
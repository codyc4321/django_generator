#!/usr/bin/env python

"""get all Django models from a single file. returns the actual full text of the model, from start to finish, doesn't return model names yet"""

from my_scripting_library import *

#----------------------------------------------------------------------------------------------------

match_info_dicts = get_all_models(CWD)
print match_info_dicts
model_names = list_models_from_info_dicts(match_info_dicts)
write_content("/tmp/classnames.txt", str(model_names))
print "\nFind your models in /tmp/classnames.txt\n"
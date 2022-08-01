#!/usr/bin/env python

import re, subprocess, sys, os
from os.path import expanduser
from my_scripting_library.silo_functions import *

LIBRARY="/home/cchilders/scripts/python/my_scripting_library"

sys.path.append(LIBRARY)

"""makes auto graphs to view relationalDB relationships"""

UNIT_PATH = "/home/cchilders/projects/advantage/unit_tests/"

apps_to_graph = sys.argv[1:]
apps_to_graph_string = " ".join(apps_to_graph)
apps_to_graph_uscore = "_".join(apps_to_graph)

parser = optparse.OptionParser()
parser.add_option('-f', '--filename', dest='filename', help='Give a different filename than the default graph.png')

(options, args) = parser.parse_args()

if options.filename:
    filename = options.filename
else:
    filename = 'graph_' + apps_to_graph_uscore + '.png'
print filename

#----------------------------------------------------------------------------------------------------

print apps_to_graph_string

call_sp("./manage.py graph_models {apps} | dot -Tpng -o {filename}".format(apps=apps_to_graph_string, filename=filename))



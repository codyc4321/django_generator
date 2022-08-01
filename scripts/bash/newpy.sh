#!/bin/bash

#takes file_name and starts it in script folder

PYSCR="/home/cchilders/scripts/python/general/in_progress"


if [ "$1" != '' ]; then
  echo '#!/usr/bin/env python' > "$PYSCR/$1.py"
  echo '# coding: utf-8' >> "$PYSCR/$1.py"
  echo '' >> "$PYSCR/$1.py"
  echo '' >> "$PYSCR/$1.py"
  echo '' >> "$PYSCR/$1.py"
  chmod +x "$PYSCR/$1.py"
  gedit "$PYSCR/$1.py"
else
  echo "Please enter a filename:"
  read NAME
  #touch "$NAME" ".py"
  echo '#!/user/bin/env python' > "$PYSCR/$NAME.py"
  echo '# coding: utf-8' >> "$PYSCR/$NAME.py"
  echo '' >> "$PYSCR/$NAME.py"
  chmod +x "$PYSCR/$NAME.py"
  gedit "$PYSCR/$NAME.py"
fi

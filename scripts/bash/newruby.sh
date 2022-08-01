#!/bin/bash

#takes file_name and starts it in script folder


RUSCR="/home/cchilders/scripts/ruby"


if [ "$1" != '' ]; then
  echo '#!/usr/bin/ruby -w' > "$RUSCR/$1.rb"
  echo "$RUSCR/$1"
  echo '' >> "$RUSCR/$1.rb"
  chmod +x "$RUSCR/$1.rb"
  gedit "$RUSCR/$1.rb"
else
  echo "Please enter a filename:"
  read NAME
  echo '#!/usr/bin/ruby -w' > "$RUSCR/$NAME.rb"
  echo '' >> "$RUSCR/$NAME.rb"
  chmod +x "$RUSCR/$NAME.rb"
  gedit "$RUSCR/$NAME.rb"
fi


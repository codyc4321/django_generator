#!/bin/bash

#takes file_name and starts it in script folder

SHSCR="/home/cchilders/scripts/bash"


if [ "$1" != '' ]; then
  SHELLPATH="$SHSCR/$1.sh"
  echo "$SHELLPATH"
  echo '#!/bin/bash' > "$SHELLPATH"
  echo '' >> "$SHELLPATH"
  echo '' >> "$SHELLPATH"
  echo '' >> "$SHELLPATH"
  chmod +x "$SHELLPATH"
  gedit "$SHELLPATH"
else
  echo "Please enter a filename:"
  read NAME
  SHELLPATH="$SHSCR/$NAME.sh"
  echo '#!/bin/bash' > "$NAME.sh"
  echo '' >> "$SHELLPATH"
  echo '' >> "$SHELLPATH"
  echo '' >> "$SHELLPATH"
  chmod +x "$SHELLPATH"
  gedit "$SHELLPATH"
fi

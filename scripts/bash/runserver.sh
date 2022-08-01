#!/bin/bash

PROJECTS="/home/cchilders/projects"

echo "$PROJECTS/$1"

cd $PROJECTS'/'$1
python manage.py runserver 


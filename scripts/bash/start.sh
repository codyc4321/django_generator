#!/bin/bash

HOME="/home/cchilders"

cd $HOME/projects/dating_site_profiles
$HOME/Downloads/Sublime\ Text\ 2/sublime_text &
python manage.py runserver &
gnome-terminal
cd $HOME/projects/dating_site_profiles
sleep 0.3
ls
google-chrome "http://127.0.0.1:8000/accounts/"
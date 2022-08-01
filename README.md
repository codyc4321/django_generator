Hi, I'm Scriptcity, the Django-app-writing-Django-app.

In your favorite text editor, open the folders `main` and `templates` to watch me work. Notice they both have a 'scripts' folder.

Go to the main folder (th folder that has manage.py) and run:
    bash install.sh

Then:
    bash run.sh

The file `robots/app_writer.py` is doing the work.

Now watch 'scripts' in both dirs disappear and reappear

Scriptcity rewrites itself in this way if you change/add/delete content.

./manage.py runserver, and visit localhost:8000 to navigate

At this stage, Scriptcity rewrites itself and displays plain format links to formatted ruby, python, or bash code grabbed from an API. It generates a basic static app that renders your file structure, so you can easily read your code.

Not all files are compatible with django template language (occasional django.template.base.TemplateSyntaxError).

Start at 'http://127.0.0.1:8000/'

#!/usr/bin/env python

"""
Writes the view, template, form, and urls for a specific model with a powerful search method from command line, 
automating the entire process of the update portion of CRUD in django. the building block of my djangomation package I'm writing. 
Flexible enough to suggest you defaults, but allow you to pick url, view names, etc. 
Run from command line as long as you're in the main dir where manage.py is. 
Basic functions already written can be easily extended to automate all django operations
"""

import time, re, os, sys
 
# from silo_of_functions import *
from my_scripting_library import *

from django.template.defaultfilters import slugify


#----------------------------------------------------------------------------------------------------

def process_matches(match_info_dicts=None, model_names=None):
    
    def _gather_edit_names(model_name=None):
        url_name        = gather(msg="Please enter a name for the url:", default="edit-{model_name}".format(model_name=model_name))
        view_name       = gather(msg="Please enter a name for the view:", default="edit_{model_name}".format(model_name=model_name))
        return url_name, view_name

    """don't break...this is already customized for this script, insert_import_statement is the reusable one"""
    def _insert_import_statements_to_formsdotpy(app_name=None, filepath=None, import_string=None):
        for root, dirs, files in os.walk(CWD):
            forms_dot_py_path = os.path.join(root, app_name, 'forms.py')
            if not 'forms.py' in files:
                insert_import_statement(forms_dot_py_path, 'from django import forms')
            insert_import_statement(forms_dot_py_path, (make_import_statement(app_name, model_names)))
            dirs[:] = []

    def _add_forms_to_formsdotpy(project_path=None, app_name=None):
        forms_dot_py_path = os.path.join(project_path, app_name, 'forms.py')
        new_form = make_model_form(d)
        append_content(forms_dot_py_path, (new_form + '\n\n'))
    
    def _handle_templates(project_path=None, app_name=None, desired_templates=None, form_name=None):
        template_code       = make_basic_form_code(form_name)
        if type(desired_templates) == str:
            template_path = os.path.join(CWD, 'templates', app_name, desired_templates)
            append_content(template_path, (template_code + '\n\n'))
        if type(desired_templates) == list:
            template_paths      = []
            for template in desired_templates:
                template_path = os.path.join(CWD, 'templates', app_name, template)
                append_content(template_path, (template_code + '\n\n'))

    for match_dict in match_info_dicts:
        #setup
        filepath            = match_dict['filepath']
        app_name            = get_folder_directly_under_other_folder(filepath, CWD)
        model_name          = match_dict['name']
        model_name_slug     = slugify(model_name)
        form_name           = model_name_slug + "_form"
        
        #gather
        url_name, view_name = _gather_edit_names(model_name=model_name_slug)
        
        #templates
        template_name       = pick_template_file(project_path=CWD, app_name=app_name, default='edit_{model_name_slug}.html'.format(model_name_slug=model_name_slug))
        template_name       = ensure_endswith(list_or_string=template_name, should_endwith='.html')
        _handle_templates(project_path=CWD, app_name=app_name, desired_templates=template_name, form_name=form_name)
        
        #forms
        _insert_import_statements_to_formsdotpy(app_name)
        new_form            = make_model_form(match_dict)
        append_django_content(project_path=CWD, app_name=app_name, filetype='forms', content=new_form)
        
        #views
        views_dot_py_path   = os.path.join(CWD, app_name, 'views.py')
        insert_import_statement(views_dot_py_path, "from django.contrib.auth.decorators import login_required\nfrom django.shortcuts import get_object_or_404")
        view_content        = make_view_edit_payload(app_name=app_name, model_name=model_name, view_name=view_name, template_name=template_name, form_name=form_name)
        append_django_content(project_path=CWD, app_name=app_name, filetype='views', content=view_content)
        
        #urls
        url_payload, url_name_text = make_url_payload(url_name=url_name, model_name=model_name, view_name=view_name)
        insert_url_payload(payload=url_payload, project_path=CWD, app_name=app_name)

        print """Register <a href="{{% url '{app_name}:{url_name_text}' {model_name_slug}.id %}}">Edit {model_name}</a>""".format(app_name=app_name, 
                                                                                                             url_name_text=url_name_text,
                                                                                                             model_name=model_name,
                                                                                                             model_name_slug=model_name_slug)


#----------------------------------------------------------------------------------------------------


settingspath = get_settings_path(CWD)
apps = get_apps(CWD)
match_info_dicts = get_desired_models_info(CWD)
model_names = list_models_from_info_dicts(match_info_dicts)
process_matches(match_info_dicts=match_info_dicts, model_names=model_names)








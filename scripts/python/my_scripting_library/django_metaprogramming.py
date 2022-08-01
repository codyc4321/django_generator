

#----------------------------------------------------------------------------------------------------

def make_import_statement(app_name, model_names):
    model_names_string = ", ".join(model_names)
    string = "from {app_name}.models import {model_names}".format(app_name=app_name, model_names=model_names_string)
    return string

#----------------------------------------------------------------------------------------------------

def make_basic_form_code(form_name):
    string = """
{{% load bootstrap %}}

{{{{ {form_name}|bootstrap }}}}
""".format(form_name=form_name)
#     string = """
# <form id="{model_name}_form" method="post" action="" enctype="multipart/form-data">
#     {{% csrf_token %}}
#     {{{{ {model_name}_form.as_p }}}}
#    <input type="submit" name="submit" value="This is the display text" />
# """.format(model_name=model_name)
    return string

#----------------------------------------------------------------------------------------------------

def make_url_payload(url_name=None, model_name=None, view_name=None):
    URL_PAYLOAD = """\n    url(r'^{url_name}/(?P<{model_name}_id>\d+)/$', views.{view_name},    name='{url_name_text}'),\n"""
    url_name_text = view_name.replace("_", "-")
    model_name_text = model_name.lower()
    payload = URL_PAYLOAD.format(model_name=model_name_text, view_name=view_name, url_name_text=url_name_text, url_name=url_name)
    return payload, url_name_text
    
#----------------------------------------------------------------------------------------------------

def insert_url_payload(project_path=None, app_name=None, payload=None):
    urls_path = os.path.join(project_path, app_name, 'urls.py')
    content = read_content(urls_path)
    payload = list_to_string(payload)
    rgx = r"urlpatterns.*(?=[)])"
    match = re.search(rgx, content, re.DOTALL)
    url_patterns_start_string = match.group().rstrip()
    if not url_patterns_start_string.endswith(','):
        url_patterns_start_string += ','
    url_patterns_start_string += payload
    new_content = re.sub(rgx, url_patterns_start_string, content, flags=re.DOTALL)
    write_content(urls_path, new_content)
    
    
#----------------------------------------------------------------------------------------------------

def get_all_fields_from_model_to_make_modelform(model_text):
    model_lines = model_text.split('\n')
    fields      = []
    print model_lines
    for line in model_lines:
        print line
        if 'DateTimeField' in line:
            continue
        if 'TimeField' in line:
            continue
        if 'DateField' in line:
            continue
        if 'objects' in line:
            continue
        field_rgx = r"^[ ]{4}(?P<field_name>\w+)\s*[=]"
        try:
            print 'we tryin'
            match = re.search(field_rgx, line)
            print match
            print match.group('field_name')
            fields.append(match.group('field_name'))
        except AttributeError:
            pass
    return fields
    
#----------------------------------------------------------------------------------------------------

def make_model_form(model_dict):
    def _make_field_tuple_string(fields):
        fields_strings_list = []
        for i, field in enumerate(fields): 
            if i % 5 == 0 and i != 0:
                fields_strings_list.append("\n                  '" + field + "'")
            else:
                fields_strings_list.append("'" + field + "'")
        fields_string = ", ".join(fields_strings_list)
        return fields_string
    
    # for model_name, model_text in model_dict.items():
    fields = get_all_fields_from_model_to_make_modelform(model_dict['class_text'])
    fields_string = _make_field_tuple_string(fields)
    model_form_string = """\n\n
class {model_name}Form(forms.ModelForm):
    class Meta:
        model = {model_name}
        fields = ({fields_string})\n\n
""".format(model_name=model_dict['name'], fields_string=fields_string)
    return model_form_string
    
#----------------------------------------------------------------------------------------------------    
    
def make_view_edit_payload(app_name=None, model_name=None, view_name=None, template_name=None, 
                           redirect_url=None, form_name=None):
    
    VIEW_EDIT_PAYLOAD = """
\n
def {view_name}(request, {model_name_slug}_id, template_name='{app_name}/{template_name}'):
    user = request.user
    {model_name_slug} = get_object_or_404({model_name}, id={model_name_slug}_id)
    {form_name} = {model_name}Form(request.POST or None, instance={model_name_slug})
    if {form_name}.is_valid():
        {model_name_slug} = {form_name}.save(commit=False)
        #do stuff
        {model_name_slug}.save()
        return redirect('{redirect_url}')
    return render(request, template_name, locals())
"""
    redirect_url = redirect_url or 'your url'
    model_name_slug = slugify(model_name)
    view_content    = VIEW_EDIT_PAYLOAD.format(model_name=model_name, view_name=view_name, 
                                               template_name=template_name, app_name=app_name,
                                               model_name_slug=model_name_slug,
                                               redirect_url=redirect_url,
                                               form_name=form_name)
    return view_content

#----------------------------------------------------------------------------------------------------

def make_view_add_payload(app_name=None, model_name=None, view_name=None, template_name=None, 
                           redirect_url=None, form_name=None):
    
    VIEW_ADD_PAYLOAD = """
\n
def {view_name}(request, {model_name_slug}_id, template_name='{app_name}/{template_name}'):
    user = request.user
    {form_name} = {model_name}Form(request.POST or None)
    if {form_name}.is_valid():
        {model_name_slug} = {form_name}.save(commit=False)
        #do stuff
        {model_name_slug}.save()
        return redirect('{redirect_url}')
    return render(request, template_name, locals())
"""
    redirect_url = redirect_url or 'your url'
    model_name_slug = slugify(model_name)
    view_content    = VIEW_ADD_PAYLOAD.format(model_name=model_name, view_name=view_name, 
                                               template_name=template_name, app_name=app_name,
                                               model_name_slug=model_name_slug,
                                               redirect_url=redirect_url,
                                               form_name=form_name)
    return view_content
    
#----------------------------------------------------------------------------------------------------

def make_view_list_objects_payload(app_name=None, model_name=None, view_name=None, template_name=None):
    
    VIEW_LIST_OBJECTS_PAYLOAD = """             
def {view_name}(request, template_name='{app_name}/{template_name}'):
    user = request.user
    {model_name_slug}s = {model_name}.objects.all()
    return render(request, template_name, locals())
"""
    model_name_slug = slugify(model_name)
    view_content    = VIEW_LIST_OBJECTS_PAYLOAD.format(model_name=model_name, view_name=view_name, 
                                               template_name=template_name, app_name=app_name,
                                               model_name_slug=model_name_slug)
    return view_content
#----------------------------------------------------------------------------------------------------

def make_view_delete_object_payload(app_name=None, model_name=None, view_name=None, list_objects_redirect=None):
    VIEW_DELETE_OBJECT_PAYLOAD = """
def {view_name}(request, {model_name_slug}_id):
    try:
        item_to_delete = {model_name}.objects.get(id={model_name_slug}_id)
        item_to_delete.delete()
    except DoesNotExist:
        pass
    return redirect('{list_objects_redirect}')
"""
    model_name_slug = slugify(model_name)
    view_content    = VIEW_DELETE_OBJECT_PAYLOAD.format(model_name=model_name, view_name=view_name, 
                                               list_objects_redirect=list_objects_redirect, 
                                               app_name=app_name,
                                               model_name_slug=model_name_slug)
    return view_content
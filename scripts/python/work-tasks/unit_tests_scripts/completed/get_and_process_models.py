#!/usr/bin/env python

import os, sys, re, time, optparse, subprocess

"""
turned ~10 days work into 2 days, having the robot write 183 django models, 
saved them a few thousand bucks by thinking in ways that surprised my coworkers

instead of clicking around from file to file, and referring back to the Faker docs every time I encountered a django field
I wasn't sure of and doublechecking if I'm using the right Faker field, while writing ~5000 lines of code by hand,
I decided to read the Faker docs once, make some mappings, and automate it all
"""

"""
Factory-boy and python's Faker, for automated unittesting

makes fake models for all models in your project path, filters by models.py or models/thisgrouping.py...


-m m (manual) writes one model from unit_tests_auto/tmp/model.txt to unit_tests_auto/tmp/write.txt

-m a (auto) writes all models in your project to unit_tests_auto/models_silo with separate files for each app or file within app/models/etc...
"""

HOMEPATH = os.path.expanduser("~")

PROJECT_PATH = "{}/projects/advantage/unit_tests".format(HOMEPATH)

BRIDGE = "{}/projects/bridge/unit_tests".format(HOMEPATH)

CENTRAL = "{}/projects/central/unit_tests".format(HOMEPATH)

ALL_PROJECT_PATHS = [PROJECT_PATH, BRIDGE, CENTRAL]

AUTOMATION_MAIN = "{}/unit_tests_auto".format(HOMEPATH)

SILO = "{}/unit_tests_auto/models_silo".format(HOMEPATH)

BASE_MODELS_SILO = "{}/unit_tests_auto/base_model_fields_silo".format(HOMEPATH)

DOCS = "{}/unit_tests_auto/documents".format(HOMEPATH)

#REAL!!!
FACTORY_PATH = "{}/projects/advantage/unit_tests/testing/factories".format(HOMEPATH)

PRETTY_PATH = "{}/scripts/python/general/completed/pretty_spacing.py".format(HOMEPATH)

COMMON_FIELD_TO_FAKE_FIELD = {
    'city':         'city()',
    'state':        'state_abbr()',
    'country':      'country()',
    'address_2':    'secondary_address()',
    'address_1':    'address()',
    'address':      'address()',
    'zip':          'zipcode()',
    'first_name':   'first_name()',
    'last_name':    'last_name()',
    'slug':         'slug()',
    'email':        'email()',
    # 'title':        'prefix()'
}

DJANGO_FIELD_TO_FAKE_FIELD = {
    r'models.TimeField\(':          'time()',
    r'models.DateTimeField\(':      'date_time()',
    r'models.DateField\(':          'date()',
    r'models.IntegerField\(':       'random_number(digits=2)',
    r'models.SmallIntegerField\(':  'random_number(digits=2)',
    r'models.PositiveIntegerField': 'random_number(digits=2)',
    r'models.BooleanField\(':       'boolean()',
    r'models.NullBooleanField\(':   'boolean()',
    r'models.EmailField\(':         'email()',
    r'models.PhoneNumberField':     'phone_number()',
    r'models.TextField':            'text(max_nb_chars=256)',
    r'models.WeightField':          'numerify(text="{}.##".format(FAKER.random_int(min=150, max=370)))',
    r'models.LengthField':          'numerify(text="##.##")',
    r'models.GenericIPAddressField':'ipv6()',
    r'CountryField\(':              'country()'
}

parser = optparse.OptionParser()
parser.add_option('-m', '--mode', dest='mode', help='"m" to run a single tempfile model to another temp file,\n\
                                                     "a" to remake all models in advantage')

(options, args) = parser.parse_args()


COMMON_KEYS = COMMON_FIELD_TO_FAKE_FIELD.keys()
COMMON_KEYS.sort()
COMMON_KEYS.reverse()

"""helper functions"""

#----------------------------------------------------------------------------------------------------

def call_sp(command, **arg_list):
    p = subprocess.Popen(command, shell=True, **arg_list)
    p.communicate()
    
#---------------------------------------------------------------------------

def if_append(list, item):
    if item:
        list.append(item)

#---------------------------------------------------------------------------

def read_lines(the_file):
    f = file(the_file, 'r')
    content = f.readlines()
    f.close()
    return content

#---------------------------------------------------------------------------

def read_content(the_file):
    f = file(the_file, 'r')
    content = f.read()
    f.close()
    return content

#------------------------------------------------------------------------------------------------------------------------

def write_lines(the_file, lines):
    f = file(the_file, 'w')
    f.writelines(lines)
    f.close

#------------------------------------------------------------------------------------------------------------------------

def write_content(the_file, content):
    f = file(the_file, 'w')
    f.write(content)
    f.close

#------------------------------------------------------------------------------------------------------------------------

def append_lines(the_file, lines):
    f = file(the_file, 'a')
    f.writelines(lines)
    f.close

#-------------------------------------------------------------------------------------------

def append_content(the_file, content):
    f = file(the_file, 'a')
    f.write(content)
    f.close

#---------------------------------------------------------------------------

def clear_content(the_file):
    f = file(the_file, 'w')
    f.write('')
    f.close

#---------------------------------------------------------------------------

def clear_folder(folder):
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f != 'README.txt':
                fullpath = os.path.join(root, f)
                clear_content(fullpath)

#---------------------------------------------------------------------------

def count_indentation(l):
    if l == '\n':
        return 0
    rgx = r"^\s+"
    match = re.match(rgx, l)
    if match:
        length = len(match.group())
        return length
    else:
        return 0

#------------------------------------------------------------------------------------------------------------------------

"""get class/model info"""

def get_model_name_and_classes(line):
    main_regex = r"^class\s+(?P<name>\w+)\((?P<classes>.*)\)"
    try:
        match = re.search(main_regex, line)
        model_name = match.group('name')
        classes = match.group('classes')
        if classes == 'models.Model':
            classes = 'DjangoModelFactory'
        return model_name, classes
    except AttributeError:
        return None, None

#------------------------------------------------------------------------------------------------------------------------

def get_extended_model_name(line):
    main_regex = r"^class\s+(?P<name>\w+)\((?P<classes>.*)\)"
    try:
        match = re.search(main_regex, line)
        model_name = match.group('name')
        return model_name
    except AttributeError:
        return None

#------------------------------------------------------------------------------------------------------------------------

def get_extended_classes(line):
    main_regex = r"^class\s+(?P<name>\w+)\((?P<classes>.*)\)"
    classes_regex = r"[A-Za-z0-9.]+"
    try:
        match = re.search(main_regex, line)
        model_name = match.group('name')
        classes = re.findall(classes_regex, match.group('classes'))
        return classes
    except AttributeError:
        return None
#---------------------------------------------------------------------------

def check_model_start(line):
    regex = r"^class\s+\w+\(models.Model"
    return re.search(regex, line)

#------------------------------------------------------------------------------------------------------------------------

def check_class_start(line):
    regex = r"^class\s+\w+\("
    return re.search(regex, line)

#----------------------------------------------------------------------------------------------------------------

def check_class_end(line):
    if not re.search(r"^#", line):
        if count_indentation(line) == 0:
            return True
    return False

#---------------------------------------------------------------------------------

def get_model_name_or_None(line):
    regex = r"^class\s+(\w+)\(models.Model"
    try:
        match = re.search(regex, line)
        return match.group(1)
    except:
        return None

#---------------------------------------------------------------------------


""""get all classes"""

def get_classes_from_file(file):

    lines                   = read_lines(file)
    currently_within_class  = False
    start_stop_tuples       = []
    current_start           = None

    for i, line in enumerate(lines):
        if currently_within_class:
            if line == '\n':
                continue
            elif check_class_start(line):
                start_stop_tuples.append((current_start, (i-1)))
                currently_within_class  = True
                current_start           = i
            elif check_class_end(line):
                start_stop_tuples.append((current_start, i))
                currently_within_class  = False
                current_start           = None
        else:
            if check_class_start(line):
                current_start           = i
                currently_within_class  = True
    else:
        if currently_within_class:
            start_stop_tuples.append((current_start, len(lines)))

    classes = []

    for tup in start_stop_tuples:
        class_lines = lines[tup[0]:tup[1]]
        this_class  = "\n".join(class_lines)
        classes.append(this_class)
    return classes

#---------------------------------------------------------------------------

"""helper functions to process individual lines"""

def check_for_default(line):
    default_regex = r"default="
    return re.search(default_regex, line)

#----------------------------------------------------------------------------------------------------

def check_for_abstract(model_lines):
    rgx = r"\s*abstract\s*[=]\s*True"
    for line in model_lines:
        if re.search(rgx, line): return True
    return False
    
#---------------------------------------------------------------------------

def check_if_enum_dict(line):
    enum_regex = r"\s*\w+\s*[=]\s*Enum\s*[(]"
    return re.search(enum_regex, line)

#---------------------------------------------------------------------------

def comment_out_default(line):
    stripped_line = line.lstrip()
    return ("    #" + stripped_line)

#---------------------------------------------------------------------------

def handle_comments(line, comment_bool):
    if comment_bool:
        new_line = comment_out_default(line)
        return new_line
    return line

#---------------------------------------------------------------------------

def check_for_property_function_to_skip(line):
    enum_regex = r"\s*\w+\s*[=]\s*property\s*[(]"
    return re.search(enum_regex, line)

#---------------------------------------------------------------------------

"""handle varname = models.CharField(..., choices=foo, ...)"""

def check_for_enum(line):
    enum_regex = r"choices=(?P<enum_dict_name>\w+)[,)]"
    enum_match = re.search(enum_regex, line)
    try:    return enum_match.group('enum_dict_name')
    except: return None
    
#----------------------------------------------------------------------------------------------------

def check_for_choices_keyword(line):
    return check_for_enum(line)
    
#----------------------------------------------------------------------------------------------------

def make_choice_keyword_suffix_from_filepath(filepath):
    filename, file_extension = os.path.splitext(filepath)
    relative_path = filename.replace('{}/projects/advantage/unit_tests/'.format(HOMEPATH), '')
    rp1 = relative_path.replace('/', '_')
    rp2 = '_' + rp1
    rp3 = rp2.upper()
    return rp3
    
#----------------------------------------------------------------------------------------------------

def make_import_as_name(filepath, choices_keyword):
    import_as_name = choices_keyword + make_choice_keyword_suffix_from_filepath(filepath)
    final = import_as_name.upper()
    return final
    
#----------------------------------------------------------------------------------------------------

def make_import_dot_path_from_filepath(filepath):
    filename, file_extension = os.path.splitext(filepath)
    relative_path = filename.replace('{}/projects/advantage/unit_tests/'.format(HOMEPATH), '')
    rp1 = relative_path.replace('/', '.')
    return rp1
    
#----------------------------------------------------------------------------------------------------

def make_import_as_statement(filepath, choices_keywords):
    import_as_tuples = []
    for c in choices_keywords:
        import_as_name = make_import_as_name(filepath, c)
        import_as_tuples.append((c, import_as_name))
    dot_path = make_import_dot_path_from_filepath(filepath)
    choices_keywords_strings_list = []
    for tup in import_as_tuples:
        choices_keywords_strings_list.append("{choices_keyword} as {import_as_name}".format(choices_keyword=tup[0], import_as_name=tup[1]))
    choices_keywords_string = ", ".join(choices_keywords_strings_list)
    return "from {dot_path} import {choices_keywords_string}\n".format(dot_path=dot_path, choices_keywords_string=choices_keywords_string)
    
#----------------------------------------------------------------------------------------------------

def grab_choices_keywords_for_file(filepath):
    lines = read_lines(filepath)
    choices_keywords = []
    for line in lines:
        if_append(choices_keywords, check_for_choices_keyword(line))
    unique_keywords = set(choices_keywords)
    return unique_keywords
    
#----------------------------------------------------------------------------------------------------

"""process lines"""

def process_CharField(line=None, variable_name=None, enum_dict=None):
    def _get_max_length(any_line):
        ml_regex = r"max_length=(?P<max_length>\d+)"
        ml = re.search(ml_regex, any_line)
        try:    return int(ml.group('max_length'))
        except: return None
    rgx = r"models.CharField"


    if re.search(rgx, line):
        enum_dict_name = check_for_enum(line)
        
        if enum_dict_name:
            if enum_dict:
                if enum_dict_name in enum_dict:
                    choices = enum_dict[enum_dict_name]
                    return "    {variable_name} = lazy_attribute(lambda x: FAKER.random_element({choices}))".format(variable_name=variable_name, choices=choices)

            try:
                return "    {variable_name} = lazy_attribute(lambda x: FAKER.random_element({choices}))".format(variable_name=variable_name, choices=enum_dict_name)
            except KeyError:
                print "couldnt find that enum dict name"

        max_length = _get_max_length(line)
        if max_length < 5:
            try:
                symbols = "?" * max_length
            #max_length is None
            except TypeError:
                print '\n\nline:'
                print 'unconventional model spacing, need to skip, do by hand, or rewrite script'
                return "    {variable_name} = UH OH"
            return "    {variable_name} = lazy_attribute(lambda x: FAKER.lexify(text=\"{symbols}\"))".format(variable_name=variable_name, symbols=symbols)
        return "    {variable_name} = lazy_attribute(lambda x: FAKER.text(max_nb_chars={max_length}))".format(variable_name=variable_name, max_length=max_length)
    else:
        return None

#---------------------------------------------------------------------------

def process_DecimalField(line, variable_name):
    def _get_decimal_places(any_line):
        dp_regex = r"decimal_places=\s*(?P<decimal_places>\d+)"
        try:
            dp = re.search(dp_regex, any_line)
            return int(dp.group('decimal_places'))
        except:
            return 2
            
    def _get_integer_digits(any_line, decimal_places):
        max_regex = r"max_digits=\s*(?P<max_digits>\d+)"
        try:
            match = re.search(max_regex, any_line)
            max_digits = match.group('max_digits')
            int_digits =  int(max_digits) - int(decimal_places)
            return int(int_digits)
        except:
            return 2            
            
        

    rgx = r"models.DecimalField"

    if re.search(rgx, line):
        decimal_places = _get_decimal_places(line)
        integer_places = _get_integer_digits(line, decimal_places)
        decimals = "#" * decimal_places
        integers = "#" * integer_places
        return "    {variable_name} = lazy_attribute(lambda x: Decimal(FAKER.numerify(text=\"{integers}.{decimals}\")))"\
        .format(variable_name=variable_name, integers=integers, decimals=decimals)
    else:
        return None

#---------------------------------------------------------------------------

def grab_relations(line):
    """grab variable names for things we should try to get_or_create to speed up tests... FKs, one-to-one, etc"""
    def _get_variable_name(line):
        indentation = count_indentation(line)
        if indentation == 4:
            rgx = r"^[ ]{4}(?P<variable_name>\w+)\s*="
            match = re.match(rgx, line)
            return match.group('variable_name') if match else None
        return None

    rgxes = [r"models.ForeignKey", r"models.OneToOneField", r"OneToOneFieldDefault"]

    variable_name = _get_variable_name(line)
    if not variable_name:
        return None
    for rgx in rgxes:
        if re.search(rgx, line):
            return variable_name
    return None

#---------------------------------------------------------------------------

def process_ForeignKey(line, variable_name=None, current_model_name=None):
    def _get_model_name(any_line):
        self_regex = r"ForeignKey\(\s*[\"']self[\"']"
        regex = r"ForeignKey\(\s*[\"']\w+[.](?P<model_name>\w+)"
        match = re.search(self_regex, any_line)
        if match:
            return 'self'
        match = re.search(regex, any_line)
        if match:
            return match.group('model_name')
        return "couldnt get model name"

    rgx = r"models.ForeignKey"

    if re.search(rgx, line):
        model_name = _get_model_name(line)
        return "    {} = factory.SubFactory('testing.factories.{}')".format(variable_name, model_name)
    else:
        return None

#---------------------------------------------------------------------------

def process_OneToOne(line, variable_name):
    def _get_model_name(any_line):
        regex = r"OneToOneField\(\s*[\"']\w+[.](?P<model_name>\w+)"
        match = re.search(regex, any_line)
        try:
            return match.group('model_name')
        except AttributeError:
            regex = r"OneToOneFieldDefault\(\s*[\"']\w+[.](?P<model_name>\w+)"
            match = re.search(regex, any_line)
            try:
                return match.group('model_name')
            except AttributeError:
                return "couldnt get model name"

    rgx     = r"models.OneToOneField"
    rgx2    = r"OneToOneFieldDefault"

    if re.search(rgx, line) or re.search(rgx2, line):
        model_name = _get_model_name(line)
        return "    {} = factory.RelatedFactory('testing.factories.{}')".format(variable_name, model_name)
    else:
        return None

#---------------------------------------------------------------------------

def process_CommaSeparatedIntegerTextField(line, variable_name):

    rgx = r"models.CommaSeparatedIntegerTextField"

    if re.search(rgx, line):
        return  """    {variable_name} = '21, 321, 4321, 54321'""".format(variable_name=variable_name)
    else:
        return None

#---------------------------------------------------------------------------

def Enum_handler(filepath):
    """ for:
        TYPES = Enum(
            P="Patient",
            S="Franchise Sales",
            U="Other",
            W="Corporate Wellness",
            N="Physician Network",
        )
    """
    #tuple_format_enum_rgx checks for :
    """
    EXERCISE_CHOICES    = Enum(
        ("S", "Sedentary"),
        ("M", "Mild"),
        ("O", "Occasional"),
        ("R", "Regular"),
    )
    \s*(?P<enum_name>\w+)\s*[=]\s*Enum[(](\s*[(][A-Za-z"']+[,]\s*[A-Za-z"']+[)][,]?\s*)+ matches the above enum up to the last )
    """
    get_tuple_format_enum_rgx = r"""\s*(?P<enum_name>\w+)\s*[=]\s*Enum[(](\s*[(][\"']?.*?[\"']?[,]\s*[\"']?.*?[\"']?[)][,]?\s*)+[)]"""
    get_tuple_choices_rgx = r"\s*[(]['\"]?(?P<choice>\w+)['\"]?[,]\s*['\"]?.*?['\"]?[)][,]?\s*"
    # entire_enum_rgx matches entire string from TYPES to the end [)], for a regular enum group like in the docstring
    entire_enum_rgx = r"\s*(?P<enum_name>\w+)\s*[=]\s*Enum[(].*?[)]"
    #matches P, S, U, W, N
    get_choices_rgx =r"(?P<choice>\w+)\s*[=]\s*[u]?[\"']"

    enum_dict = {}
    content = read_content(filepath)
    tuple_format_enum_generator = re.finditer(get_tuple_format_enum_rgx, content, flags=re.DOTALL)
    for thing in tuple_format_enum_generator:
        enum_text = thing.group()
        enum_name = thing.group('enum_name')
        try:
            choices = re.findall(get_tuple_choices_rgx, enum_text)
            enum_dict[enum_name] = choices
        except:
            break
    enum_generator = re.finditer(entire_enum_rgx, content, flags=re.DOTALL)
    for thing in enum_generator:
        enum_text = thing.group()
        enum_name = thing.group('enum_name')
        if enum_name in enum_dict.keys():
            continue
        try:
            choices = re.findall(get_choices_rgx, enum_text)
            enum_dict[enum_name] = choices
        except:
            break
    return enum_dict

#---------------------------------------------------------------------------

def process_line(this_line, enum_dict=None):
    def _get_variable_name(line):
        indentation = count_indentation(line)
        if indentation == 4:
            rgx = r"^[ ]{4}(?P<variable_name>\w+)\s*="
            match = re.match(rgx, line)
            return match.group('variable_name') if match else None
        return None

    #enums are dicts used as choices in CharFields
    enum_or_not = check_if_enum_dict(this_line)
    if enum_or_not:
        return 0

    # skip: "exam = property(get_exam)"
    if check_for_property_function_to_skip(this_line):
        return 0

    variable_name = _get_variable_name(this_line)
    #objects is a special manager declaration, like custom querysets etc
    if not variable_name or variable_name == 'objects':
        return 0

    has_default = check_for_default(this_line)

    for key in COMMON_KEYS:
        if key in variable_name:
            string = "    {} = lazy_attribute(lambda x: FAKER.{})".format(variable_name, COMMON_FIELD_TO_FAKE_FIELD[key])
            return handle_comments(string, has_default)

    django_field_regexes = DJANGO_FIELD_TO_FAKE_FIELD.keys()
    for regex in django_field_regexes:
        if re.search(regex, this_line):
            string = "    {} = lazy_attribute(lambda x: FAKER.{})".format(variable_name, DJANGO_FIELD_TO_FAKE_FIELD[regex])
            return handle_comments(string, has_default)

    decimal_field = process_DecimalField(this_line, variable_name)
    if decimal_field:
        return handle_comments(decimal_field, has_default)

    char_field = process_CharField(line=this_line, variable_name=variable_name, 
                                   enum_dict=enum_dict)
    if char_field:
        return handle_comments(char_field, has_default)

    foreign_key = process_ForeignKey(this_line, variable_name)
    if foreign_key:
        return foreign_key

    one_to_one = process_OneToOne(this_line, variable_name)
    if one_to_one:
        return one_to_one

    comma_separated = process_CommaSeparatedIntegerTextField(this_line, variable_name)
    if comma_separated:
        return comma_separated

    return "    {} = UNKNOWN_FIELD".format(variable_name)



#---------------------------------------------------------------------------

"""process classes"""

def make_fake_model_header(app_name=None, model_name=None, classes=None, relations=None, abstract=False):

    header = "class {model_name}({classes}):\n    class Meta:\n        model = '{app_name}.{model_name}'\n".format(model_name=model_name, classes=classes, app_name=app_name)

    if relations:
        header += "        django_get_or_create = {relations}\n".format(relations=relations)
        
    if abstract:
        header += "        abstract = True\n"
    
    return header.split("\n")

#---------------------------------------------------------------------------

def process_class(class_lines=None ,app_name=None, enum_dict=None):

    """do these 5 little irregularly filed models by hand, much faster than monkeypatching"""
    BANNED_MODELS = ['ClinicMarginOffset', 'OnlineOrder', 'OnlineOrderProduct','OnlineCoupon', 'OnlineProduct']

    if type(class_lines) == str:
        class_lines = class_lines.split('\n')
    # base_model_name = None
    # extended_model_name = None
    # extended_classes = None
    
    for this_line in class_lines:
        # base_model_name = get_base_model_name(this_line)
        # if base_model_name:
        #     break
        #smash back into one, remember to return
        model_name, classes = get_model_name_and_classes(this_line)
        # extended_classes    = get_extended_classes(this_line)
        if model_name:
            break
    
    """manual mode makes 1 model at a time...never break it"""
    # model_name = base_model_name  or extended_model_name
    if model_name in BANNED_MODELS:
        if options.mode == 'a':
            return None

    if not model_name:
        if options.mode == 'a':
            return None

    abstract = check_for_abstract(class_lines)

    new_fake_model_lines = []

    relations_to_get_or_create = []
    for l in class_lines:
        relation = grab_relations(l)
        if relation:
            relations_to_get_or_create.append(relation)
    relation_tup = tuple(relations_to_get_or_create)
    header = make_fake_model_header(app_name=app_name,
                                    model_name=model_name,
                                    classes=classes,
                                    relations=relation_tup,
                                    abstract=abstract)

    for line in header:
        new_fake_model_lines.append(line)
    for this_line in class_lines:
        new_line = process_line(this_line, enum_dict=enum_dict)
        if new_line:
            new_fake_model_lines.append(new_line)
    return '\n'.join(new_fake_model_lines)

#---------------------------------------------------------------------------

def get_app_label_off_model(model_lines):
    if type(model_lines) == str:
        model_lines = model_lines.split('\n')
    rgx = r"app_label\s*[=]\s*['](?P<app_label>\w+)[']"
    for l in model_lines:
        match = re.search(rgx, l)
        if match:
            return match.group('app_label')
    return None

#---------------------------------------------------------------------------

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

#---------------------------------------------------------------------------

"""process everything"""

def get_all_base_model_names(project_paths=[]):
    """need model names to know which ones extend, like:
            class GeocodedModel(models.Model):
                ...etc...

            class Clinic(models.PhoneDisplayMixin, GeocodedModel):
                [I have all GeocodedModel's fields too, plus my own]
                ...etc...
    """

    base_models_names = ""
    base_models_names_list = []
    for project_path in project_paths:
        for root, dirs, files in os.walk(project_path):
            for f in files:
                filepath = os.path.join(root, f)
                filename, file_extension = os.path.splitext(filepath)
                if file_extension != '.py':
                    continue
                lines = read_lines(filepath)
                for line in lines:
                    model_name = get_base_model_name(line)
                    if model_name:
                        base_models_names += model_name + '\n'
                        base_models_names_list.append(model_name)
    return base_models_names_list

#---------------------------------------------------------------------------

def get_all_models_in_advantage(project_path):
    
    #...unit_tests/records/models/invoice.py --> emr
    def _strip_project_name_and_filename_off_app(fullpath):
        app_with_models_folder_match = re.search(r'/models$', fullpath)
        if app_with_models_folder_match:
            rightstrip = app_with_models_folder_match.group()
            rightstripped = fullpath.replace(rightstrip, '')
            slash_app_name = rightstripped.replace(project_path, '')
            app_name = slash_app_name.replace('/', '')
            return app_name
        return "couldnt_find_an_app_name"

    #...unit_tests/chart/models.py --> chart
    def _lstrip_project_name_off_app(fullpath):
        app_with_models_dot_py_match = re.search(r'^{project_path}/\w+$'\
                                       .format(project_path=project_path), fullpath)
        if app_with_models_dot_py_match:
            app_name = fullpath.replace((project_path + '/'), '')
            return app_name
        return None
    
    #...unit_tests/chart/models.py --> chart.models
    def make_dotpath(fullpath):
        filename, file_extension = os.path.splitext(fullpath)
        slash_app_name = filename.replace(project_path, '')
        app_name = slash_app_name.replace('/', '.')
        app_name = app_name.replace('models.', '')
        return app_name


    for root, dirs, files in walklevel(project_path, level=2):

        for f  in files:
            filepath = os.path.join(root, f)
            filename, file_extension = os.path.splitext(filepath)
            if file_extension != '.py':
                continue
            if f == 'models.py':
                enum_dict = Enum_handler(filepath)
                app_name = _lstrip_project_name_off_app(root)
                classes = get_classes_from_file(filepath)
                if app_name:
                    writepath = os.path.join(SILO, app_name)
                    append_content(writepath, '\n\n\n\n{}\n\n'.format(filepath))
                for this_class in classes:
                    if not app_name:
                        class_lines = this_class.split('\n')
                        app_name = get_app_label_off_model(class_lines)
                    if not app_name:
                        fake_model = process_class(class_lines=this_class, app_name='no_app_name', enum_dict=enum_dict)
                        if not fake_model:
                            continue
                        docpath = os.path.join(DOCS, 'orphan_models')
                        append_content(docpath, 'Not able to find an app name for {}'\
                                                .format(filepath))
                        append_content(docpath, '\n\n\n')

                        append_content(docpath, fake_model)
                        call_sp("{prettypath} {writepath}".format(writepath=writepath, prettypath=PRETTY_PATH))
                    fake_model = process_class(class_lines=this_class, app_name=app_name, enum_dict=enum_dict)
                    if not fake_model:
                        continue
                    writepath = os.path.join(SILO, app_name)
                    append_content(writepath, '\n\n')
                    append_content(writepath, fake_model)
                    append_content(writepath, '\n\n')
                    call_sp("{prettypath} {writepath}".format(writepath=writepath, prettypath=PRETTY_PATH))

        for this_dir in dirs:
            dir_path = os.path.join(root, this_dir)
            if this_dir == 'models':
                app_name = _strip_project_name_and_filename_off_app(dir_path)
                for root, dirs, files in os.walk(dir_path):
                    for f in files:
                        if not f.endswith('.py'):
                            continue
                        filepath = os.path.join(root, f)
                        writepath = os.path.join(SILO, app_name, f)
                        append_content(writepath, '\n\n\n{}\n\n'.format(filepath))
                        enum_dict = Enum_handler(filepath)
                        classes = get_classes_from_file(filepath)
                        for this_class in classes:
                            fake_model = process_class(class_lines=this_class, app_name=app_name, enum_dict=enum_dict)
                            if not fake_model:
                                continue
                            append_content(writepath, fake_model)
                            append_content(writepath, '\n\n\n')
                            call_sp("{prettypath} {writepath}".format(writepath=writepath, prettypath=PRETTY_PATH))

#-----------------------------------------------------------------------------------------------

def process_temp_model():
    TEMP_PATH       = "{}/unit_tests_auto/tmp/model.txt".format(HOMEPATH)
    TEMP_WRITE_PATH = "{}/unit_tests_auto/tmp/write.txt".format(HOMEPATH)
    model_content = read_content(TEMP_PATH)
    enum_dict = Enum_handler(TEMP_PATH)
    fake_model = process_class(class_lines=model_content, app_name='extras', enum_dict=enum_dict)
    write_content(TEMP_WRITE_PATH, fake_model)
    call_sp("{prettypath} {writepath}".format(writepath=TEMP_WRITE_PATH, prettypath=PRETTY_PATH))

#-----------------------------------------------------------------------------------------------


if not options.mode:
    while True:
        mode = raw_input("Select an option, m for manual or a for automatic: ")
        if mode in ['a', 'm']:
            options.mode = mode
            break
            
if options.mode == 'a':
    clear_folder(SILO)
    get_all_models_in_advantage(PROJECT_PATH)
elif options.mode == 'm':
    process_temp_model()

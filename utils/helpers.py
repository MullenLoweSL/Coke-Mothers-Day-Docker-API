import inspect
import re
import json
import tempfile
import pathlib
import re
import os
import datetime


def snake_case_to_upper_camel_case(snake_str):
    tmp = to_camel_case(snake_str)
    return tmp[0].upper() + tmp[1:]

def first_character_upper_case_only(in_string):
    return in_string[0].upper() + in_string[1:]

def to_camel_case(snake_str):
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])

def get_variable_name(p):
    """https://stackoverflow.com/a/592849"""
    """https://stackoverflow.com/questions/592746/how-can-you-print-a-variable-name-in-python"""
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
        if m:
            return m.group(1)

regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
match_iso8601 = re.compile(regex).match

def full_state(main_state: str, nested_state: str):
    return main_state + '_' + nested_state

def is_production():
    environment = get_env()
    return True if environment == 'prd' else False

def get_env():
    environment = os.environ.get('PYTHON_ENV')
    return environment.lower()

def starts_with_one_of(in_string: str, list_of_strings_to_match):
    for s in list_of_strings_to_match:
        if in_string.startswith(s):
            return True
    return False

def get_app_host():
    return os.environ.get('APP_HOST')

def get_default_paraplanner_id(dealer_group: str):

    if is_production():
        prd_default_paraplanner_ids = {
            'ri': '1c61a3aa-6b96-422d-8dd3-a13830fda655',
            'consultum': 'a86ef426-0f4e-40b3-9951-bff5407c1373',
            'bridges': '44e8e388-0a02-4bad-bfef-73e31837279d',
            'fsp': 'e8383ac1-51ca-471b-8375-4b22085442b5',
            'lonsdale': '5c7ae189-2833-49a8-84c4-99f69c17dc83',
            'm3': 'af06ce5a-3a2f-4bda-b1a1-928f7fcb6716',
        }
        return prd_default_paraplanner_ids[dealer_group]
    
    _env = get_env()
    if _env == "stg":
        stg_default_paraplanner_ids = {
            'ri': '4f03a0c2-8b94-4cee-adff-9869a949740b'
        }
        return stg_default_paraplanner_ids[dealer_group]
    else:
        return None

def to_iso8601_from_string(timestamp_string: str):
    """Returns an ISO string for IST"""
    timestamp_int = int(timestamp_string)
    d = datetime.datetime.utcfromtimestamp(timestamp_int)
    
    # add 5h30 to convert to IST
    timedelta = datetime.timedelta(hours=5, minutes=30)
    d += timedelta

    _d = d.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return _d

def get_path_for_temporary_file():
    filepath = tempfile.NamedTemporaryFile().name
    path = pathlib.Path(filepath)
    return str(path.parent) + '/'

def string_to_boolean(string: str, default:bool = False):
    if string is None:
        return default
    string = string.strip()
    return True if string.lower() == 'true' else False

def is_weekday(datetime_obj: datetime.datetime):
    day_of_week_id = datetime_obj.weekday()
    return True if day_of_week_id < 5 else False

def add_business_days(start_date: datetime.datetime, num_business_days: int):
    """Returns the num_business_days'th business day after start_date
    e.g start_date = "Friday 9 AM", num_business_days = 1 => final_date = "Monday 9 AM"
    """
    final_date = start_date
    while num_business_days > 0:
        final_date += datetime.timedelta(days=1)        
        if is_weekday(final_date):
            num_business_days -= 1
    return final_date

def is_valid_iso8601(str_val):
    try:
        if match_iso8601( str_val ) is not None:
            return True
    except:
        pass
    return False

def datetime_as_string(datetime_obj: datetime.datetime):
    """Returns a string like 01/23/21"""
    return datetime_obj.strftime('%d/%m/%y')

def timestamp_from_datetime_object(datetime_obj: datetime.datetime):
    return datetime_obj.timestamp()

def is_valid_timestamp(x):
    if x is None:
        return False 

    try:
        _ = datetime.datetime.fromtimestamp(int(x))
    except ValueError:
        return False
    else:
        return True
    
def is_float_or_int(x):
    # check type equality first
    if isinstance(x, float):
        return True 
    if isinstance(x, int):
        return True 
    
    # cast string 
    if isfloat(x):
        return True 
    if isint(x):
        return True 
    
    return False
    
def isfloat(x):
    try:
        _ = float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True

def isint(x):
    try:
        a = float(x)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b

def section_title_from_section_key(section_key: str) -> str:
    sections_dict = {"superannuation": "Superannuation",
                     "retirementIncome": "Retirement Income",
                     "nonSuperInvestments": "Non-super Investments",
                     "debt": "Debt",
                     "cashFlowManagement": "Cash Flow Management",
                     "socialSecurity": "Social Security",
                     "insurance": "Insurance",
                     "estatePlanning": "Estate Planning",
                     "smsf": "SMSF",
                     "agedCare": "Aged Care",
                     "familyTrust": "Family Trust"}
    
    # return key itself if not found    
    return sections_dict.get(section_key, section_key)
    
def convert_dict_of_dicts_to_list_of_dicts(input_dict: dict) -> list:
    return [value for value in input_dict.values()]

def remove_dict_keys_by_prefix(input_dict, prefix):
    tmp_input_dict = input_dict.copy()
    res = list(tmp_input_dict.keys()) 
    for key in res: 
        if key.startswith(prefix): 
            tmp_input_dict.pop(key)
    return tmp_input_dict

def clean_azure_response(input_dict):
    return remove_dict_keys_by_prefix(input_dict, "_")

def camelcase_to_snakecase(input_str):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', input_str).lower()

def convert_dict_keys_camelcase_to_snakecase(input_dict):
    tmp_input_dict = input_dict.copy()
    res = list(tmp_input_dict.keys()) 
    for camelcase_key in res: 
        snakecase_key = camelcase_to_snakecase(camelcase_key)
        tmp_input_dict[snakecase_key] = tmp_input_dict[camelcase_key]
        del tmp_input_dict[camelcase_key]
    return tmp_input_dict

def format_currency(value: float, prepend_dollar: bool=False):
    if prepend_dollar:
        return '${0:,.2f}'.format(value)
    else:
        return '{0:,.2f}'.format(value)

def get_file_names_from_list_of_file_upload_results(file_upload_results_list: list):
    files_string = ', '.join([file_upload.name for file_upload in file_upload_results_list])
    return files_string

def get_filename_from_filepath(filepath: str):
    _, tail = os.path.split(filepath)
    return tail

def get_extension_from_filename(filename: str):
    return filename.split(".")[-1]

def get_file_list_from_file_dict_list(file_dict_list: dict):
    """Retuns a list of filenames, given a list of file dictionaries
    It assumes: the id and name are "id" and "name" respectively
    e.g. 
    [
        {
            "id": "c403ce41-82e1-4565-a570-7b3d566f646e",
            "name": "3c-checkbox-unselected.pdf (1)"
        },
        {
            "id": "d403ce41-82e1-4565-a570-7b3d566f646e",
            "name": "da-checkbox-unselected.pdf (1)"
        }
    ]
    
    Returns an empty list if the input is None
    """
    if file_dict_list is None:
        return list()
    return [file_dict['name'] for file_dict in file_dict_list]

def candidate_dict_keys_match(candidate_dict: dict, required_dict: dict):
    # TODO: Make this work for dicts with nested dicts!
    # Returns TRUE if:
    #   all keys and nested keys in required_dict exist in candidate_dict
    #   all corresponding values and nested values in required_dict exist are the same as candidate_dict
    # and FALSE otherwise
    for key in required_dict:
        if key not in candidate_dict:
            return False
        if candidate_dict[key] != required_dict[key]:
            return False
    return True

def get_list_of_placeholders(text):
    regex = r"\{{(.*?)\}}"
    matches = re.finditer(regex, text)

    list_of_placeholders = []
    for _, match in enumerate(matches):
        for _ in range(0, len(match.groups())):
            list_of_placeholders.append("{{" + match.group(1) + "}}")
    
    return list_of_placeholders

def extract_dict_from_select_placeholder(placeholder):
    # test_str = "%owner%, create a {{select.var5:[binding: binding, nonbinding: non-binding, nonlapsing: non-lapsing]}} beneficiary."
    regex = r"\[(.*?)\]"
    matches = re.findall(regex, placeholder)

    dict_entries = matches[0].split(",")
    dropdown_dict = {}
    for entry in dict_entries:
        splitted_entry = entry.split(":")
        entry_key = splitted_entry[0].strip()
        entry_value = splitted_entry[1].strip()
        dropdown_dict.update({entry_key:entry_value})
        
    return dropdown_dict
    
def extract_variable_from_select_placeholder(placeholder):
    # "text": "%owner%, retain {{number.var0}} in {{select.var1:[{xplan-products}]}}"
    # "text": "%owner%, create a {{select.var5:[binding: binding, nonbinding: non-binding, nonlapsing: non-lapsing]}} beneficiary."
    regex = r"\.(.*?)\:"
    matches = re.findall(regex, placeholder)
    return matches[0]
        
def extract_value_from_date_placeholder(date_pair: str):
    # example value of date_pair = "id:agePension" or "date:02/2020"
    # date_key = date_pair.split(':')[0]
    # not processing the value of date_key
    date_value = date_pair.split(':')[1]
    return date_value

def placeholder_is_date(placeholder):
    return True if "{{date" in placeholder else False

def extract_variable_from_generic_placeholder(placeholder):
    # "text": "%owner%, retain {{text.var0}}"
    # "text": "%owner%, retain {{number.var0}}"
    # "text": "%owner%, in {{date.var2}} nominate someone."
    # 
    # Handle the possibility of there being placeholder text (only possible for generic (non-select) placeholders)
    # e.g.
    # {{number.var0:Enter a dollar value here}}
    # {{text.var1:Enter your account here}}
    
    if generic_placeholder_contains_placeholder_text(placeholder=placeholder):
        regex = r"\.(.*?)\:"
    else:
        regex = r"\.(.*?)\}"
    matches = re.findall(regex, placeholder)
    return matches[0]

def placeholder_is_xplan_select(placeholder):
    return True if "{xplan-products}" in placeholder else False

def generic_placeholder_contains_placeholder_text(placeholder):
    # This assumes the placeholder is a generic (non-select) placeholder
    # i.e. there is no ":" present
    return True if ":" in placeholder else False
    
def placeholder_is_dropdown_type(placeholder):
    """"Return True if this placeholder is of type: select, invselect or invflipselect"""
    if "{{select" in placeholder or "{{invselect" in placeholder or "{{invflipselect" in placeholder:
        return True
    return False

def placeholder_is_custom_select(placeholder):
    """"Return True if this placeholder is of type: invselect or invflipselect"""
    if "{{invselect" in placeholder or "{{invflipselect" in placeholder:
        return True
    return False

def is_currency_placeholder(placeholder, value: str = None):
    #  Update: we have added a "{{text_currency}}" placeholder now
    # this syncs data to the backend WITH the dollar sign, commas, etc
    # therefore:
    #   - we don't need to ever use this method - therefore always returning False,
    #   - comment all previous code
    return False

    # # since some dollar values are captured via the {{text}} placeholder, we need to inspect the value itself,
    # # to decide if we should render it as a currency.
    # # If it is an int or float, assume it was a dollar amount entered
    # return True if "{{text_currency" in placeholder or is_float_or_int(value) else False

def replace_string_with_formatting(string, string_to_find, string_to_replace, make_bold=False, make_currency=False):
    # if string_to_replace is empty string, replace with dash
    if not string_to_replace:
        string_to_replace = "-"
    if make_currency:
        string_to_replace = "$" + format_currency(float(string_to_replace))
    if make_bold:
        string_to_replace = "<b>" + str(string_to_replace) + "</b>"
    return string.replace(string_to_find, string_to_replace)

def policy_type_from_policy(policy: str):
    policy_type = policy.split('_')[0]
    if policy_type == 'life' or policy_type == 'trauma':
        return policy_type.capitalize()
    else:
        # TPD/IP
        return policy_type.upper()

def increment_dictionary_count(original_dict: dict, delta_dict: dict):
    result = dict(original_dict)
    for k,v in delta_dict.items():
        if k not in result:
            result[k] = v
        else:
            result[k] += v
    return result


def get_cur_dir():
    return os.getcwd()

def write_json(file_prefix, data_dict, filename=None, directory=None):
    # writes content to file in folder
	# {{file_prefix}}_%m-%d-%y %H:%M:%S.json
    if filename is None:
        now = datetime.datetime.now()
        now = now.strftime('%m-%d-%y_%H-%M')
        filename = file_prefix + '_' + now + '.json'

    if directory is None:
        directory = get_cur_dir()
        
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w') as outfile:
        json.dump(data_dict, outfile, indent=4)
    return filename

def read_json(filename, directory=None):
	# reads content from directory with filename
    if directory is None:
        directory = get_cur_dir()

    filepath = os.path.join(directory, filename)
    with open(filepath) as f:
        data = json.load(f)
    return data
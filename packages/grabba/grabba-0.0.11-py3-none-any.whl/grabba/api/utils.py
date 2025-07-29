import re

def camel_to_snake(name: str) -> str:
    """Convert camelCase string to snake_case"""
    # Handle acronyms (e.g., 'JSONData' → 'json_data')
    name = re.sub('([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
    # Handle normal camelCase (e.g., 'camelCase' → 'camel_case')
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()

def to_camel_case(snake_str):
    """Convert snake_case to camelCase"""
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])

def dict_to_camel_case(data, skip_regex=None):
    """
    Recursively convert dictionary keys to camelCase.
    skip_regex: Keys matching this pattern won't be converted (but their children will be)
    """
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            current_key_skipped = bool(skip_regex and re.match(skip_regex, str(key)))
            # Only skip conversion of THIS key if it matches the pattern
            new_key = key if current_key_skipped else to_camel_case(key)
            # Run "dict_to_camel_case" recursively
            new_dict[new_key] = dict_to_camel_case(
                value, 
                skip_regex=skip_regex,
            )
        return new_dict
    elif isinstance(data, list):
        return [dict_to_camel_case(item, skip_regex) for item in data]
    else:
        return data
    
def dict_to_snake_case(data, skip_regex=None):
    """
    Recursively convert dictionary keys to snake_case.
    skip_regex: Keys matching this pattern won't be converted (but their children will be)
    parent_key_skipped: Internal flag to track if we're under a skipped key
    """
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            current_key_skipped = bool(skip_regex and re.match(skip_regex, str(key)))
            # Only skip conversion of THIS key if it matches the pattern
            new_key = key if current_key_skipped else camel_to_snake(key)            
            # Run "dict_to_snake_case" recursively
            new_dict[new_key] = dict_to_snake_case(
                value, 
                skip_regex=skip_regex
            )
        return new_dict
    elif isinstance(data, list):
        return [dict_to_snake_case(item, skip_regex) for item in data]
    else:
        return data

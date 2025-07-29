def list_to_tuple(my_type):
    def convert(l):
        return tuple(my_type(x) for x in l)
    return convert


def list_to_tuple(my_type):
    def convert(l):
        return tuple(my_type(x) for x in l)
    return convert

def get_first_value(d, keys, default=None):
    for key in keys:
        val = d.get(key)
        if val is not None and val != '':
            return val
    return default


def get_unique_key(key, d):
    """
    Generate a unique key for a dictionary by appending a numeric suffix.

    Args:
    key (str): The original key.
    d (dict): The dictionary in which the key needs to be unique.

    Returns:
    str: A unique key.
    """
    if key not in d:
        return key
    i = 1
    while f"{key}-{i}" in d:
        i += 1
    return f"{key}-{i}"
from typing import List, Dict, Any


def flatten_nested_dict(nested_dict: Dict[str, Any], parent_key: str = '', sep: str = '.' ) -> Dict[str, Any]:
    """
    Flattens a nested dictionary into a single level dictionary.
    Keys are concatenated with a specified separator.
    
    :param nested_dict: The nested dictionary to flatten.
    :param parent_key: The base key string to use for nested keys.
    :param sep: The separator to use for concatenation of keys.
    :return: A flattened dictionary.
    """
    items = []
    for k, v in nested_dict.items():
        new_key = f'{parent_key}{sep}{k}' if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_nested_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def generate_random_numbers(count: int, low: int, high: int) -> List[int]:
    """
    Generates a list of random integers.
    
    :param count: The number of random integers to generate.
    :param low: The lower bound for random integer generation.
    :param high: The upper bound for random integer generation.
    :return: A list containing generated random integers.
    """
    import random
    return [random.randint(low, high) for _ in range(count)]


def is_valid_username(username: str) -> bool:
    """
    Checks if a username is valid based on Roblox's requirements.
    
    :param username: The username to validate.
    :return: True if the username is valid, otherwise False.
    """
    return username.isalnum() and 3 <= len(username) <= 20

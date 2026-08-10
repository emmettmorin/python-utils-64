def safe_divide(num, denom):
    try:
        if denom == 0:
            raise ValueError('Denominator cannot be zero')
        return num / denom
    except TypeError:
        raise TypeError('Both numerator and denominator must be numbers')


def parse_json(json_string):
    import json
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        raise ValueError('Invalid JSON string provided')


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f'The file {file_path} was not found')
    except IOError:
        raise IOError(f'An error occurred while reading the file {file_path}')
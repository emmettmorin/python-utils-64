import json
import re

def validate_input(user_input):
    if not isinstance(user_input, str):
        return False
    if len(user_input) < 3:
        return False
    if not re.match('^[a-zA-Z0-9_]+$', user_input):
        return False
    return True

def process_input(user_input):
    if validate_input(user_input):
        # Simulating processing
        return f'Processed: {user_input}'
    else:
        raise ValueError('Invalid input')

def main_loop():
    user_inputs = ['validInput1', 'bad input', 'ab', 'validInput2']
    results = []
    for input_str in user_inputs:
        try:
            result = process_input(input_str)
            results.append(result)
        except ValueError as e:
            results.append(str(e))
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main_loop()
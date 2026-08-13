import json
import re

def validate_input(data):
    if not isinstance(data, dict):
        raise ValueError('Input must be a dictionary')
    if 'username' not in data or not isinstance(data['username'], str):
        raise ValueError('Username must be a string')
    if not re.match('^[a-zA-Z0-9_]{3,20}$', data['username']):
        raise ValueError('Username must be 3-20 characters long and can only contain letters, numbers, and underscores')
    if 'age' in data:
        if not isinstance(data['age'], int) or not (0 <= data['age'] <= 120):
            raise ValueError('Age must be an integer between 0 and 120')

def main_processing_loop(inputs):
    results = []
    for input_data in inputs:
        try:
            validate_input(input_data)
            # hypothetical processing logic
            results.append(f"Processed {input_data['username']}")
        except ValueError as ve:
            results.append(f"Error: {ve}")
    return results

if __name__ == '__main__':
    test_inputs = [
        {'username': 'user1', 'age': 25},
        {'username': 'user@name', 'age': 30},
        {'username': 'us', 'age': -5},
        {'username': 'user2'}
    ]
    output = main_processing_loop(test_inputs)
    print(json.dumps(output, indent=4))
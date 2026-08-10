class ValidationError(Exception):
    pass

def validate_input(data):
    if not isinstance(data, dict):
        raise ValidationError('Input must be a dictionary')
    if 'name' not in data or not isinstance(data['name'], str):
        raise ValidationError('Missing or invalid name')
    if 'age' not in data or not isinstance(data['age'], int) or data['age'] <= 0:
        raise ValidationError('Missing or invalid age')

if __name__ == '__main__':
    inputs = [{'name': 'Alice', 'age': 30}, {'name': 123, 'age': 25}, {'name': 'Bob', 'age': -5}]
    for input_data in inputs:
        try:
            validate_input(input_data)
            print(f'Validated: {input_data}')
        except ValidationError as e:
            print(f'Validation failed: {e}')
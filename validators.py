def validate_input(data):
    if not isinstance(data, dict):
        raise ValueError("Input must be a dictionary")
    if 'username' not in data:
        raise ValueError("Missing 'username' key")
    if 'age' in data and (not isinstance(data['age'], int) or data['age'] <= 0):
        raise ValueError("Age must be a positive integer")
    if 'email' in data:
        if not isinstance(data['email'], str) or '@' not in data['email']:
            raise ValueError("Invalid email format")
    return True

def main_loop(data_list):
    for data in data_list:
        try:
            validate_input(data)
            process_data(data)
        except ValueError as e:
            print(f"Input error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


def process_data(data):
    print(f"Processing data for user: {data['username']}")

if __name__ == '__main__':
    sample_data = [
        {'username': 'User1', 'age': 25, 'email': 'user1@example.com'},
        {'username': 'User2', 'age': -5},
        {'username': 'User3', 'email': 'invalidemail'},
        {'username': 'User4'}
    ]
    main_loop(sample_data)
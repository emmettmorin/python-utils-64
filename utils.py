import json
import re

def validate_username(username):
    if not isinstance(username, str):
        raise ValueError('Username must be a string')
    if len(username) < 3 or len(username) > 20:
        raise ValueError('Username must be between 3 and 20 characters')
    if not re.match('^[a-zA-Z0-9_]+$', username):
        raise ValueError('Username can only contain alphanumeric characters and underscores')
    return True

def main_processing_loop(usernames):
    valid_usernames = []
    for username in usernames:
        try:
            validate_username(username)
            valid_usernames.append(username)
        except ValueError as e:
            print(f'Invalid username '{username}': {str(e)}')
    return valid_usernames

if __name__ == '__main__':
    test_usernames = ['user_1', 'invalid@user', 'us', 'a_very_long_username_123']
    print(main_processing_loop(test_usernames))
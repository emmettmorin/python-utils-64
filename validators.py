def validate_input(user_input):
    if not isinstance(user_input, dict):
        return False, "Input must be a dictionary"
    required_keys = ['name', 'age', 'email']
    for key in required_keys:
        if key not in user_input:
            return False, f"Missing required key: {key}"
        if key == 'age' and (not isinstance(user_input[key], int) or user_input[key] < 0):
            return False, "Age must be a non-negative integer"
        if key == 'email' and '@' not in user_input[key]:
            return False, "Invalid email format"
    return True, "Valid input"

def main_processing_loop():
    while True:
        user_input = get_user_input()
        is_valid, message = validate_input(user_input)
        if not is_valid:
            print(message)
            continue
        process_valid_input(user_input)

if __name__ == '__main__':
    main_processing_loop()
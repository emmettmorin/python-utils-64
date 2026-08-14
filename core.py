import json

class RobloxInput:
    def __init__(self, user_input):
        self.user_input = user_input

    def validate(self):
        if not isinstance(self.user_input, str):
            raise ValueError('Input must be a string')
        if len(self.user_input) > 100:
            raise ValueError('Input must not exceed 100 characters')
        if not self.user_input.strip():
            raise ValueError('Input cannot be empty or whitespace')
        return True

class RobloxProcessor:
    def __init__(self):
        self.results = []

    def process_input(self, user_input):
        input_validator = RobloxInput(user_input)
        try:
            if input_validator.validate():
                processed = f'Processed: {user_input}'
                self.results.append(processed)
                return processed
        except ValueError as e:
            return str(e)

if __name__ == '__main__':
    processor = RobloxProcessor()
    inputs = ['test', '   ', 123, 'another valid input']
    for user_input in inputs:
        result = processor.process_input(user_input)
        print(result)
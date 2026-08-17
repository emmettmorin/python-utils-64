def calculate_discount(price, discount):
    if discount < 0 or discount > 100:
        raise ValueError('Discount must be between 0 and 100')
    return price - (price * (discount / 100))


def format_price(price):
    return f'${price:.2f}'


def is_valid_username(username):
    return username.isalnum() and 3 <= len(username) <= 20


def sanitize_input(user_input):
    return ''.join(char for char in user_input if char.isalnum() or char in (' ', '_'))


def find_max(numbers):
    if not numbers:
        return None
    max_number = numbers[0]
    for number in numbers:
        if number > max_number:
            max_number = number
    return max_number


def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)
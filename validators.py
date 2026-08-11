import re

class Validator:
    def __init__(self):
        self.email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        self.phone_pattern = re.compile(r"^\+?[1-9]\d{1,14}$")

    def is_valid_email(self, email):
        return bool(self.email_pattern.match(email))

    def is_valid_phone(self, phone):
        return bool(self.phone_pattern.match(phone))

    def validate_multiple_emails(self, emails):
        return [email for email in emails if self.is_valid_email(email)]

    def validate_multiple_phones(self, phones):
        return [phone for phone in phones if self.is_valid_phone(phone)]

# Example usage
if __name__ == '__main__':
    validator = Validator()
    valid_emails = validator.validate_multiple_emails(['test@example.com', 'invalid-email', 'user@domain.org'])
    valid_phones = validator.validate_multiple_phones(['+1234567890', '12345', '+987654321'])
    print(valid_emails)
    print(valid_phones)
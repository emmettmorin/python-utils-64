# Python Utils 64

Python Utils 64 is a collection of versatile utility functions designed to streamline common programming tasks in Python projects. With a focus on performance and simplicity, this library helps developers enhance productivity and write cleaner, more efficient code.

## Features

- **Data Validation**: Quickly validate and sanitize input data with built-in functions for strings, numbers, and other types.
- **File Operations**: Simplify reading from and writing to files with easy-to-use methods that handle different formats (CSV, JSON, and TXT).
- **Date and Time Utilities**: Manipulate and format dates and times effortlessly using a range of helper functions to enhance temporal data handling.
- **HTTP Requests Simplification**: Make HTTP requests easier with a set of functions that manage common tasks such as GET, POST, and error handling.

## Installation

To install Python Utils 64, you can use pip. Open your terminal and run the following command:

```bash
pip install python-utils-64
```

## Basic Usage Example

Here’s a quick example demonstrating some of the functionalities offered by Python Utils 64:

```python
from python_utils_64 import data_validation, file_operations, date_utils

# Data Validation
email = "user@example.com"
if data_validation.is_valid_email(email):
    print(f"{email} is valid.")

# File Operations
file_operations.write_to_file('data.txt', 'Hello, World!')
content = file_operations.read_from_file('data.txt')
print(content)

# Date Utilities
formatted_date = date_utils.format_date(datetime.now())
print(f"Current Date: {formatted_date}")
```

## License

View the [MIT License](https://opensource.org/licenses/MIT) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) for more details.

For more information on usage and detailed documentation, please check the wiki or the code comments within the project. Contributions are welcome; feel free to submit a pull request!
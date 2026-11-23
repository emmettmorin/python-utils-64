# python-utils-64

A lightweight, high-performance Python toolkit designed to streamline Roblox development workflows and API interactions. This library simplifies complex data processing tasks, making it easier to interface with Roblox’s ecosystem programmatically.

## Features

*   **RBX-Asset Downloader:** Automated fetching and parsing of asset metadata and content from the Roblox CDN.
*   **Cookie Session Manager:** Secure handling of `.ROBLOSECURITY` tokens with built-in validation and CSRF token extraction.
*   **DataStore Batch Processor:** Optimized serialization tools for interacting with Roblox DataStore APIs in bulk.
*   **Rate-Limit Awareness:** Intelligent request throttling to ensure compliance with Roblox API documentation while maintaining high throughput.

## Installation

Install `python-utils-64` via pip:

```bash
pip install python-utils-64
```

To include dependencies for advanced authentication, use:

```bash
pip install python-utils-64[auth]
```

## Usage

Below is a simple example demonstrating how to initialize a session and fetch user information:

```python
from python_utils_64 import RobloxClient

# Initialize client with your session token
client = RobloxClient(cookie="YOUR_ROBLOSECURITY_TOKEN")

# Fetch authenticated user profile
user = client.get_authenticated_user()
print(f"Logged in as: {user.name} (ID: {user.id})")

# Example: Get game pass information
pass_info = client.get_game_pass_details(1234567)
print(f"Pass Price: {pass_info.price} Robux")
```

## Contributing

Contributions are welcome! Please open an issue to discuss proposed changes or submit a pull request with unit tests.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.
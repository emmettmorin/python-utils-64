# python-utils-64

`python-utils-64` is a lightweight Python toolkit designed to streamline interactions with the Roblox ecosystem. It simplifies complex API tasks, allowing developers to manage assets, player data, and game configurations with minimal overhead.

## Features

*   **Roblox Cookie Authenticator:** Securely manage sessions using session cookies with automated CSRF token handling.
*   **Asset Uploader:** Rapidly batch upload images, decals, or audio files to the Roblox creator dashboard via the internal API.
*   **Game State Monitor:** Real-time polling utilities to track server status, player counts, and API health endpoints.
*   **DataStore Interop:** Efficient helper methods for interacting with Roblox DataStore V2, including custom serialization and batch querying.

## Installation

Install the package directly via pip:

```bash
pip install python-utils-64
```

To work with the latest features from the development branch:

```bash
git clone https://github.com/Developer/python-utils-64.git
cd python-utils-64
pip install -r requirements.txt
```

## Basic Usage

The following example demonstrates how to initialize a client and fetch details for a specific Roblox place:

```python
from utils64 import RobloxClient

# Initialize with your session cookie
client = RobloxClient(cookie=".ROBLOSECURITY_TOKEN_HERE")

# Fetch game metadata
place_info = client.games.get_place_details(place_id=123456789)

print(f"Game Name: {place_info.name}")
print(f"Active Players: {place_info.player_count}")
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
# python-utils-64

`python-utils-64` is a lightweight Python toolkit designed to streamline interactions with the Roblox ecosystem. It simplifies complex API tasks, allowing developers to automate workflows and manage game data with minimal boilerplate code.

### Features

*   **Cookie-based Authentication:** Securely initialize sessions for Roblox API requests with built-in CSRF token handling.
*   **Asset Management:** Automated utilities for uploading and updating decals, meshes, and audio assets directly from your local filesystem.
*   **DataStore Interfacing:** Robust wrappers for interacting with Roblox DataStores, including batch retrieval and error-resilient writing.
*   **Universe Stats:** High-level functions to fetch real-time analytics, concurrent player counts, and server-side configurations.

### Installation

Install `python-utils-64` directly via pip:

```bash
pip install python-utils-64
```

To install from source for development:

```bash
git clone https://github.com/Developer/python-utils-64.git
cd python-utils-64
pip install .
```

### Usage

Below is a simple example of how to authenticate and fetch the current player count for a specific universe:

```python
from python_utils_64 import RobloxClient

# Initialize the client with your .ROBLOSECURITY cookie
client = RobloxClient(cookie="YOUR_COOKIE_HERE")

# Fetch real-time analytics for a specific Universe ID
universe_id = 123456789
stats = client.get_universe_stats(universe_id)

print(f"Current players online: {stats.playing}")
```

### License

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
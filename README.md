# python-utils-64

`python-utils-64` is a lightweight Python toolkit designed to streamline interactions with the Roblox ecosystem. It provides robust wrappers for common API tasks and data processing workflows for developers.

### Features

*   **Asset Handling:** Simplified functions for fetching metadata, images, and configuration data from Roblox assets via public APIs.
*   **RBXL Parser:** Native support for parsing and traversing `.rbxl` file structures without requiring Roblox Studio.
*   **Data Serialization:** Optimized utility methods for handling Roblox's unique `JSON` format and `Luau` table serialization.
*   **Rate-Limit Awareness:** Built-in backoff logic and session management for frequent requests to the Roblox Web API.

### Installation

Install the package directly via pip:

```bash
pip install python-utils-64
```

To install from source for local development:

```bash
git clone https://github.com/Developer/python-utils-64.git
cd python-utils-64
pip install -e .
```

### Usage

Here is a quick example of how to fetch asset information using the library:

```python
from python_utils_64 import AssetClient

client = AssetClient()

# Retrieve metadata for a specific model or decal
asset_info = client.get_asset_info(123456789)

print(f"Asset Name: {asset_info['Name']}")
print(f"Creator: {asset_info['Creator']['Name']}")
```

### Requirements
*   Python 3.8+
*   `requests` library

### License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License - see the `LICENSE` file for details.
# python-utils-64

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`python-utils-64` is a high-performance Python library designed for Roblox developers to streamline external data encoding, asset management, and Luau-compatible serialization. It simplifies complex interactions with Roblox Open Cloud APIs and optimizes data payload handling for external databases and webhooks.

## Features

* **Luau Table Serializer**: Convert complex Python dictionaries and lists directly into optimized Luau table strings for seamless ingestion by Roblox servers.
* **Open Cloud Wrapper**: Simplified interface for interacting with Roblox Datastores, MessagingService, and Place Publishing APIs.
* **RBXM/RBXMX Parser**: Deconstruct and analyze binary and XML Roblox model files directly within Python environments.
* **Security Validation**: Built-in validation utilities for checking `.ROBLOSECURITY` cookie expiration and API key permissions.

## Installation

Install the package via pip:

```bash
pip install python-utils-64
```

## Quick Start

Here is a quick example of how to validate a cookie and serialize game data for a Roblox Datastore using `python-utils-64`:

```python
from python_utils_64 import RobloxClient, LuauSerializer

# Initialize the client using Roblox Open Cloud
client = RobloxClient(api_key="your_open_cloud_api_key")

# Format Python data into a Luau-compatible table string
player_data = {
    "username": "Builderman",
    "level": 75,
    "inventory": ["Sword", "Shield", "Potion"]
}
luau_string = LuauSerializer.to_table(player_data)
print(luau_string)
# Output: {username = "Builderman", level = 75, inventory = {"Sword", "Shield", "Potion"}}

# Publish data to a Roblox Datastore
datastore = client.get_datastores(universe_id=123456789)
datastore.set_entry(
    datastore_name="PlayerData", 
    key="User_2", 
    value=player_data
)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
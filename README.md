# python-utils-64

A high-performance Python toolkit designed for Roblox developers to streamline data manipulation and API interactions. This library simplifies complex workflows, allowing for faster integration between local Python environments and the Roblox ecosystem.

## Features

*   **RBXL Parser:** Efficiently read and process `.rbxl` file structures without needing the Roblox Studio client.
*   **Asset Management:** Automated scripts for bulk-uploading textures and decals to the Roblox Creator Dashboard via the Open Cloud API.
*   **Datastore Sync:** Seamlessly bridge external databases with Roblox Datastores, supporting key-value serialization for game persistence.
*   **Luau Syntax Checker:** Built-in linting integration to validate script segments before pushing to Rojo-managed projects.

## Installation

Install the package via pip:

```bash
pip install python-utils-64
```

To enable the Open Cloud API integration, ensure you have your API Key exported in your environment:

```bash
export ROBLOX_API_KEY='your-api-key-here'
```

## Basic Usage

Quickly fetch your game's current player count or metadata using the library:

```python
from roblox_utils import RobloxClient

client = RobloxClient(api_key="your_key")

# Retrieve place information
place_info = client.get_place_metadata(place_id=123456789)
print(f"Current server count: {place_info.active_servers}")

# Push a bulk update to the datastore
client.datastore.update_entry("PlayerData", "user_123", {"level": 50})
```

## License

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
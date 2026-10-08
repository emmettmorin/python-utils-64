[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

# python-utils-64

A high-performance Python utility library designed specifically for Roblox developers to streamline backend data management, Luau-compatible serialization, and API interactions. It bridges the gap between external Python services and Roblox game servers by providing robust, type-safe wrappers for Roblox web APIs and asset pipelines.

## Features

* **Luau Data Serializer:** Convert complex Python dictionaries and objects directly into optimized, valid Luau table strings for seamless ingestion by game servers.
* **RBXLX Parser:** Parse and modify XML-format Roblox place files (`.rbxlx`) programmatically, ideal for automated build systems and CI/CD pipelines.
* **Universe API Wrapper:** Fast, asynchronous helper functions for updating developer products, managing datastores, and dispatching Open Cloud messaging.

## Installation

Install the package directly from PyPI:

```bash
pip install python-utils-64
```

## Quick Start

The following example demonstrates how to serialize a Python dictionary into a Luau table and dispatch it to a Roblox server via the Open Cloud API.

```python
from python_utils_64 import LuauSerializer, OpenCloudClient

# 1. Serialize Python data to Luau table format
player_data = {
    "username": "Builderman",
    "inventory": ["Sword", "Shield"],
    "stats": {"Level": 50, "XP": 2450}
}
luau_table = LuauSerializer.to_table(player_data)
print(luau_table) 
# Output: {username = "Builderman", inventory = {"Sword", "Shield"}, stats = {Level = 50, XP = 2450}}

# 2. Dispatch data to game servers using Open Cloud
client = OpenCloudClient(api_key="mpb_928374982374928374")
client.publish_topic(
    universe_id=123456789,
    topic="PlayerDataUpdate",
    data=luau_table
)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---
*Maintained by Developer.*
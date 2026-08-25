# python-utils-64

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

python-utils-64 is a Python library tailored for Roblox developers, offering robust utilities to interact with Roblox's ecosystem. The package handles API requests, asset management, and file parsing to accelerate development and automation tasks.

## Features
- Authenticated access to Roblox APIs with automatic token management
- Efficient downloading and caching of Roblox assets
- Support for reading and writing Roblox XML and binary formats
- Rate limit handling and retry mechanisms for reliable operations

## Installation

Install via pip:

```bash
pip install python-utils-64
```

Install from source:

```bash
git clone https://github.com/developer/python-utils-64.git
cd python-utils-64
pip install -e .
```

## Basic Usage

```python
from python_utils_64 import RobloxClient

client = RobloxClient()
game = client.get_game(1234567890)
print(f"Game name: {game.name}")
print(f"Player count: {game.playing}")
```
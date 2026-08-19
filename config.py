import json
import os

class ConfigLoader:
    def __init__(self, default_config):
        self.default_config = default_config
        self.config = self.default_config.copy()

    def load(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                try:
                    user_config = json.load(file)
                    self.config.update(user_config)
                except json.JSONDecodeError:
                    print('Invalid JSON in configuration file')

    def get(self, key, default=None):
        return self.config.get(key, default)

    def __repr__(self):
        return json.dumps(self.config, indent=4)

# Example default configuration
default_config = {
    'setting1': 'value1',
    'setting2': 'value2',
    'setting3': 'value3'
}

# Usage
config_loader = ConfigLoader(default_config)
config_loader.load('config.json')

# Accessing a setting
print(config_loader.get('setting1'))
print(config_loader)
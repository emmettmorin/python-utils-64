import json
import os

class ConfigLoader:
    def __init__(self, config_file='config.json', default_config=None):
        self.config_file = config_file
        self.default_config = default_config if default_config else {}
        self.config = self.load_config()

    def load_config(self):
        config = self.default_config.copy()
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                try:
                    user_config = json.load(file)
                    config.update(user_config)
                except json.JSONDecodeError:
                    print('Error: Invalid JSON in config file. Using defaults.')  
        return config

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as file:
            json.dump(self.config, file, indent=4)

# Usage example
if __name__ == '__main__':
    defaults = {'log_level': 'INFO', 'output_dir': './logs'}
    config_loader = ConfigLoader(default_config=defaults)
    print(config_loader.config)

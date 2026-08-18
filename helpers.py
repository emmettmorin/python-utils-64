import json

class ConfigLoader:
    def __init__(self, default_config):
        self.default_config = default_config
        self.loaded_config = default_config.copy()

    def load(self, json_file_path):
        try:
            with open(json_file_path, 'r') as json_file:
                file_config = json.load(json_file)
                self._merge_configs(file_config)
        except FileNotFoundError:
            print(f'Config file not found: {json_file_path}')
        except json.JSONDecodeError:
            print(f'Error decoding JSON from the file: {json_file_path}')

    def _merge_configs(self, file_config):
        for key, value in file_config.items():
            if key in self.default_config:
                self.loaded_config[key] = value

    def get_config(self):
        return self.loaded_config

# Example usage:
# default_config = {'setting1': 'default_value', 'setting2': 42}
# loader = ConfigLoader(default_config)
# loader.load('config.json')
# config = loader.get_config()  
# print(config)
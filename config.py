import json
import os

class ConfigLoader:
    def __init__(self, default_config_path):
        self.default_config = self.load_json(default_config_path)
        self.user_config = {}

    def load_json(self, path):
        with open(path, 'r') as file:
            return json.load(file)

    def load_user_config(self, user_config_path):
        if os.path.exists(user_config_path):
            self.user_config = self.load_json(user_config_path)

    def get_config(self):
        return {**self.default_config, **self.user_config}

    def save_user_config(self, path):
        with open(path, 'w') as file:
            json.dump(self.user_config, file, indent=4)

if __name__ == '__main__':
    loader = ConfigLoader('default_config.json')
    loader.load_user_config('user_config.json')
    final_config = loader.get_config()
    print(final_config)
from typing import Dict, Any

class Config:
    """
    A class to manage configuration settings for the application.
    """

    def __init__(self, settings: Dict[str, Any]) -> None:
        """
        Initializes the configuration with the provided settings.

        Parameters:
        settings (Dict[str, Any]): A dictionary containing configuration settings.
        """
        self.settings = settings

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves the value for a given key from the settings.

        Parameters:
        key (str): The key for the desired setting.
        default (Any): The default value to return if the key does not exist. Defaults to None.

        Returns:
        Any: The value associated with the key, or the default value if the key does not exist.
        """
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Sets the value for a given key in the settings.

        Parameters:
        key (str): The key of the setting to modify.
        value (Any): The new value to set for the key.
        """
        self.settings[key] = value

    def all(self) -> Dict[str, Any]:
        """
        Returns all settings.

        Returns:
        Dict[str, Any]: A dictionary of all configuration settings.
        """
        return self.settings

# Example usage:
# config = Config({'max_players': 100, 'game_mode': 'survival'})
# print(config.get('max_players'))  # Outputs: 100
# config.set('max_players', 150)
# print(config.all())  # Outputs: {'max_players': 150, 'game_mode': 'survival'}
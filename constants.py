from typing import Final

# Constants related to Roblox game development

# The base URL for the Roblox API
ROBLOX_API_URL: Final[str] = 'https://api.roblox.com/'

# Commonly used exception messages
INVALID_USER_ID: Final[str] = 'The user ID provided is invalid.'

# Default values for various game settings
DEFAULT_GAME_NAME: Final[str] = 'Untitled Game'
DEFAULT_MAX_PLAYERS: Final[int] = 10

# Roblox user permission levels
class PermissionLevel:
    ADMIN: Final[str] = 'Admin'
    MODERATOR: Final[str] = 'Moderator'
    USER: Final[str] = 'User'

# Game genres
class GameGenre:
    ADVENTURE: Final[str] = 'Adventure'
    FPS: Final[str] = 'First-Person Shooter'
    RPG: Final[str] = 'Role-Playing Game'
    SIMULATION: Final[str] = 'Simulation'

# HTTP status codes for Roblox API responses
class HttpStatus:
    OK: Final[int] = 200
    NOT_FOUND: Final[int] = 404
    INTERNAL_SERVER_ERROR: Final[int] = 500



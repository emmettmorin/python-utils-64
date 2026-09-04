import math
from typing import Final, Union, Dict

# Roblox-specific constants and physics heuristics
GRAVITY: Final[float] = 196.2
CLIENT_FPS: Final[int] = 60
NETWORK_TICK: Final[float] = 1 / 20

# Roblox coordinate space scaling
STUD_TO_METERS: Final[float] = 0.28

# Bitmask helpers for CollisionGroup identifiers
COLLISION_LAYERS: Final[Dict[str, int]] = {
    "DEFAULT": 1,
    "PLAYER": 2,
    "NPC": 4,
    "PROJECTILE": 8,
    "ENVIRONMENT": 16
}

def get_raycast_params(filter_list: list, ignore_water: bool = True) -> dict:
    """Factory for standardized Roblox raycast parameters."""
    return {
        "FilterType": 1 if ignore_water else 0,
        "FilterDescendantsInstances": filter_list,
        "IgnoreWater": ignore_water
    }

def calculate_trajectory(v0: float, theta: float, dist: float) -> float:
    """Predict height at distance using kinematics."""
    angle_rad = math.radians(theta)
    return (dist * math.tan(angle_rad)) - (GRAVITY * (dist**2) / (2 * (v0 * math.cos(angle_rad))**2))

# Standardized status codes for Roblox API responses
STATUS_MAP: Final[Dict[int, str]] = {
    200: "OK",
    403: "TOKEN_EXPIRED",
    429: "RATE_LIMITED",
    503: "SERVICE_UNAVAILABLE"
}
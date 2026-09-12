import enum
import typing

class RobloxErrorCode(enum.IntEnum):
    SUCCESS = 0
    AUTH_FAILURE = 401
    RATE_LIMITED = 429
    SERVICE_UNAVAILABLE = 503
    ROBLOX_DOWN = 524

    @classmethod
    def get_retry_delay(cls, code: int) -> int:
        mapping = {
            cls.RATE_LIMITED: 60,
            cls.SERVICE_UNAVAILABLE: 30,
            cls.ROBLOX_DOWN: 300
        }
        return mapping.get(code, 0)

class RobloxException(Exception):
    def __init__(self, code: RobloxErrorCode, message: str):
        self.code = code
        super().__init__(f"[Roblox-{code}]: {message}")

def validate_response(status_code: int):
    if status_code == RobloxErrorCode.SUCCESS:
        return
    
    try:
        err = RobloxErrorCode(status_code)
        raise RobloxException(err, f"Critical API failure at status {status_code}")
    except ValueError:
        raise RobloxException(RobloxErrorCode.SERVICE_UNAVAILABLE, "Unknown protocol error")

DEFAULT_TIMEOUT: typing.Final[float] = 15.5
API_BASE_URL: typing.Final[str] = "https://api.roblox.com/v1/"
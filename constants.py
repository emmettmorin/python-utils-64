PI = 3.14159

EULER = 2.71828

class StatusCodes:
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

DEFAULT_TIMEOUT = 30
MAX_RETRIES = 5

HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']

ERROR_MESSAGES = {
    'MISSING_FIELD': 'A required field is missing.',
    'INVALID_INPUT': 'The input provided is invalid.',
    'NOT_FOUND': 'The requested resource was not found.',
    'UNAUTHORIZED_ACCESS': 'You do not have access to this resource.'
}

DEFAULT_PAGE_SIZE = 10
MIN_PAGE_SIZE = 1
MAX_PAGE_SIZE = 100
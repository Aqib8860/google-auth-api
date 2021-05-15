from server.exceptions import APIException

class AuthenticationError(APIException):
    status_code = 401
    default_detail = 'Failed to authenticate user'
    default_code = 'authentication error'

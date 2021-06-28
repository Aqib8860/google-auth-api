def _get_codes(detail):
    if isinstance(detail, list):
        return [_get_codes(item) for item in detail]
    elif isinstance(detail, dict):
        return {key: _get_codes(value) for key, value in detail.items()}
    return detail.code


def _get_full_details(detail):
    if isinstance(detail, list):
        return [_get_full_details(item) for item in detail]
    elif isinstance(detail, dict):
        return {key: _get_full_details(value) for key, value in detail.items()}
    return {
        'message': detail,
        'code': detail.code
    }

class APIException(Exception):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    status_code = 500
    default_detail = 'A server error occurred.'
    default_code = 'error'

    def __init__(self, detail=None, code=None):
        if detail is None:
            self.detail = self.default_detail
        if code is None:
            self.code = self.default_code

        self.detail = detail

        # self.detail = _get_error_details(detail, code)

    def __str__(self):
        return str(self.detail)

    def get_codes(self):
        """
        Return only the code part of the error details.

        Eg. {"name": ["required"]}
        """
        return _get_codes(self.detail)

    def get_full_details(self):
        """
        Return both the message & code parts of the error details.

        Eg. {"name": [{"message": "This field is required.", "code": "required"}]}
        """
        return _get_full_details(self.detail)
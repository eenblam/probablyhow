class RequestError(Exception):
    def __init__(self, message, url=None):
        super(RequestError, self).__init__(message)
        self.url = url

class CannotCompleteRequestError(Exception):
    """Raise when failure of current function breaks API call chain"""

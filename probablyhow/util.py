class RequestError(Exception):
    def __init__(self, message, url=None):
        super(RequestError, self).__init__(message)
        self.url = url

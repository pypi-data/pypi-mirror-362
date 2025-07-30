class RestClientException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code
        self.message = message


class RestClientHTTPException(RestClientException):
    def __init__(self, status_code: int, message: str):
        super().__init__(message=message, status_code=status_code)

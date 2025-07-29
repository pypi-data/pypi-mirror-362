class LastFMError(Exception):
    pass

class LastFMHTTPError(LastFMError):
    def __init__(self, status_code: int, message: str):
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code

class LastFMAPIError(LastFMError):
    def __init__(self, code: int, message: str):
        super().__init__(f"Last.fm API Error {code}: {message}")
        self.code = code
        self.message = message

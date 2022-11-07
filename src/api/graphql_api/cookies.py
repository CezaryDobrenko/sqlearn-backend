class CookieService:
    path: str
    http_only: bool
    request: object
    cookie_session: object

    def __init__(self, context: dict, path: str = "/", http_only: bool = True):
        self.cookie_session = context.get("cookie_session")
        self.request = context.get("request")
        self.http_only = http_only
        self.path = path

    def set_refresh_token(self, refresh_token: str) -> None:
        self.cookie_session["set_cookie"] = self._create_cookie(
            "refresh_token", refresh_token
        )

    def get_cookie(self, key: str) -> str:
        return self.request.cookies.get(key)

    def _create_cookie(self, name: str, value: str) -> str:
        cookie_string = f"{name}={value};Path={self.path};"
        if self.http_only:
            cookie_string += "HttpOnly"
        return cookie_string

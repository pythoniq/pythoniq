class Factory:
    # Create a new cookie instance.
    def make(self, name: str, value: str, minutes: int = 0, path: str = None, domain: str = None, secure: bool = None,
             httpOnly: bool = True, raw: bool = False, sameSite: str | None = None):
        pass

    # Create a cookie that lasts "forever" (five years).
    def forever(self, name: str, value: str, path: str = None, domain: str = None, secure: bool = None,
                httpOnly: bool = True, raw: bool = False, sameSite: str | None = None):
        pass

    # Expire the given cookie.
    def forget(self, name: str, path: str = None, domain: str = None) -> None:
        pass

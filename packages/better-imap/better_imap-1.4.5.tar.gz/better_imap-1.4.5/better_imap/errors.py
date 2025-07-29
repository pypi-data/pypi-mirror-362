class BetterImapException(Exception):
    pass


class IMAPLoginFailed(BetterImapException):
    def __init__(self, msg: str = None):
        msg = f". {msg}" if msg else ""
        super().__init__(
            f"IMAP disabled or account banned or incorrect login/password {msg}"
        )


class IMAPSearchTimeout(BetterImapException):
    pass


class UnknownEmailDomain(BetterImapException):
    def __init__(self, email: str):
        super().__init__(f"Unknown email domain {email}")

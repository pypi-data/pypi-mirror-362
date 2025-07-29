"""Exception raised when an invalid TOTP key is encountered."""


class InvalidTOTPKeyError(Exception):
    """Exception raised when an invalid TOTP key is encountered."""

    def __init__(self):
        """Initialize the invalid TOTP key error."""
        super().__init__("Invalid TOTP key")

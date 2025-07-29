from platform import system


class UnsupportedPlatformException(Exception):
    """Exception raised when an unsupported platform is encountered."""

    def __init__(self):
        """Initialize the unsupported platform exception."""
        super().__init__(f"Unsupported platform: {system()}")

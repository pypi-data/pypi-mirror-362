class BitwardenNotInstalledError(Exception):
    """Exception raised when the Bitwarden CLI is not installed."""

    def __init__(self):
        """Initialize the Bitwarden not installed error."""
        super().__init__("Bitwarden CLI is not installed.")

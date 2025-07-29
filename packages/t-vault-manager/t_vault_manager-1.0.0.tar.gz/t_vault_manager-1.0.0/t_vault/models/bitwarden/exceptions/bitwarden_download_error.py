"""Exception raised when a download operation fails."""


class BitwardenDownloadError(Exception):
    """Exception raised when a download operation fails."""

    def __init__(self):
        """Initialize the Bitwarden download error."""
        super().__init__("Failed to download Bitwarden.")

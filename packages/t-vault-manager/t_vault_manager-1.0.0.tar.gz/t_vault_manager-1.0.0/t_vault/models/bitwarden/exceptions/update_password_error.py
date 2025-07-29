class UpdatePasswordError(Exception):
    """Exception raised when an error occurs during a password update operation."""

    def __init__(self, name: str):
        """Initialize the update password error."""
        super().__init__(f"Failed to update password for {name}")

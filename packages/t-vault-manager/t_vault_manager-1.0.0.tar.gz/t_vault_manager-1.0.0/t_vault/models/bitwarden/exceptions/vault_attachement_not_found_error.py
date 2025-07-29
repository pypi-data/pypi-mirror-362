class VaultAttatchmentNotFoundError(Exception):
    """Exception raised when an attachment is not found."""

    def __init__(self, attachment_name: str):
        """Initialize the vault attachment not found error."""
        super().__init__(f"Attachment '{attachment_name}' not found.")

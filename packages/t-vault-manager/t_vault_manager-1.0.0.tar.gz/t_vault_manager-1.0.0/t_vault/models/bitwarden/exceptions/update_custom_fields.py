class UpdateCustomFieldsError(Exception):
    """Exception raised when an error occurs with custom fields."""

    def __init__(self):
        """Initialize the update custom fields error."""
        super().__init__("Failed to update custom fields.")

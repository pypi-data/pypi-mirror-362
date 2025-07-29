from abc import ABC, abstractmethod
from binascii import Error as BadBase32Error
from re import search

from pyotp import TOTP
from t_object import ThoughtfulObject

from . import Attachment
from .exceptions import InvalidTOTPKeyError


class VaultItem(ThoughtfulObject, ABC):
    """A class representing a vault item."""

    name: str = ""
    item_id: str = ""
    totp_key: str | None = None
    attachments: list[Attachment] = []
    fields: dict[str, str | None] = {}
    url: str | None = None
    url_list: list[str] = []
    username: str | None = None
    password: str | None = None

    @abstractmethod
    def get_attachment(self, attachment_name: str, file_path: str) -> str:
        """Get an attachment by name.

        Args:
            attachment_name: The name of the attachment to retrieve.
            file_path: The path to save the attachment to.

        Returns:
            str: The path to the downloaded attachment.
        """
        raise NotImplementedError()

    @abstractmethod
    def update_password(self, password: str | None = None) -> str:
        """Update the password of the vault item.

        Args:
            password: The new password. If None, a new password will be generated.

        Returns:
            str: The new password.
        """
        raise NotImplementedError()

    def update_custom_fields(self, fields: dict | None = None) -> dict:
        """Update the custom fields of the vault item.

        Args:
            fields: The new custom fields.

        Returns:
            dict: The new custom fields.

        """
        raise NotImplementedError()

    @property
    def otp_now(self) -> str | None:
        """Returns the current TOTP code generated using the TOTP key associated with the instance.

        Returns:
            str: The current TOTP code, or None if no TOTP key is set.
        """
        try:
            return TOTP(self.totp_key.replace(" ", "")).now() if self.totp_key else None
        except BadBase32Error as e:
            if match := search(r"secret=([A-Z0-9]+)", self.totp_key):
                return TOTP(match[1]).now()
            raise InvalidTOTPKeyError() from e

    def __getitem__(self, key):
        """Get an item by key.

        Args:
            key: The key to retrieve the item.

        Returns:
            The item corresponding to the key, or the username if key is "login".
        """
        if key == "login":
            return self.username
        try:
            return self.fields[key]
        except KeyError:
            return getattr(self, key)

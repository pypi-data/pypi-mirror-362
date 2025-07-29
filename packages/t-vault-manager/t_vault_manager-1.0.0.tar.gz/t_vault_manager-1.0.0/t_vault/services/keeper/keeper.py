"""Keeper vault service integration.

This module provides a singleton service for interacting with Keeper Commander,
a password management platform. It handles authentication, two-factor authentication,
device approval, and record retrieval operations.

The service extends Keeper's ConsoleLoginUi to provide automated handling of
authentication flows including TOTP-based 2FA and device approval.
"""

from time import time
from typing import Type

from keepercommander.api import login, sync_down
from keepercommander.auth import login_steps
from keepercommander.error import KeeperApiError
from keepercommander.loginv3 import console_ui
from keepercommander.params import KeeperParams
from keepercommander.vault import KeeperRecord
from pyotp import TOTP

from ...models.keeper import KeeperCredentials
from ...utils import logger
from ...utils.core import singleton
from .core import TKeeperRecord


@singleton
class Keeper(console_ui.ConsoleLoginUi):
    """Keeper Commander service for password vault operations.

    This singleton service provides an interface to Keeper Commander vault operations
    including authentication, record retrieval, and automated handling of two-factor
    authentication flows.

    The service extends ConsoleLoginUi to override authentication methods and provide
    automated handling of 2FA using TOTP codes, eliminating the need for manual
    console interaction during authentication.

    Attributes:
        keeper_params (KeeperParams): Internal Keeper parameters instance.
        keeper_credentials (KeeperCredentials): Stored credentials for authentication.
    """

    @property
    def keeper_params(self) -> KeeperParams:
        """Get the Keeper parameters instance.

        Returns:
            KeeperParams: The authenticated Keeper parameters containing session
                         information, vault data, and other configuration.
        """
        return self._keeper_params

    @property
    def keeper_credentials(self) -> KeeperCredentials:
        """Get the stored Keeper credentials.

        Returns:
            KeeperCredentials: The credentials object containing username, password,
                              and TOTP key used for authentication.
        """
        return self._keeper_credentials

    def __init__(self):
        """Initialize the Keeper service."""
        super().__init__()
        self._last_totp_code = None
        self._last_totp_time = 0

    def _get_fresh_totp_code(self):
        """Get a fresh TOTP code, using next time period if current was recently used."""
        current_time = time()
        totp = TOTP(self.keeper_credentials.totp_key)

        # TOTP codes change every 30 seconds
        current_totp_period = int(current_time // 30)
        last_totp_period = int(self._last_totp_time // 30)

        # If we're in the same 30-second period as the last code and used very recently
        if (
            current_totp_period == last_totp_period
            and self._last_totp_code is not None
            and current_time - self._last_totp_time < 5
        ):  # Only if used very recently
            # Generate code for the NEXT time period instead of waiting
            logger.debug("Using next TOTP period to avoid code reuse")
            fresh_code = totp.at(current_time + 30)  # Next 30-second period
        else:
            # Generate code for current time period
            fresh_code = totp.now()

        self._last_totp_code = fresh_code
        self._last_totp_time = current_time

        return fresh_code

    def login(self, credentials: KeeperCredentials) -> KeeperParams:
        """Authenticate with Keeper and initialize the vault session.

        Performs login to Keeper using the provided credentials, handles the
        authentication flow including any required 2FA, and synchronizes the
        vault data from the server.

        Args:
            credentials (KeeperCredentials): Credentials object containing username,
                                           password, and TOTP key for authentication.

        Returns:
            KeeperParams: The authenticated Keeper parameters instance containing
                         session information and vault data.

        Raises:
            KeeperApiError: If authentication fails or API calls encounter errors.
        """
        keeper_params = KeeperParams()
        keeper_params.user = credentials.username
        keeper_params.password = credentials.password
        self._keeper_credentials = credentials

        try:
            login(keeper_params, login_ui=self)
        except KeeperApiError as e:
            # Sometimes OTP is expired or there are timing issues, so we need to try again
            logger.warning(f"Initial login attempt failed: {e}, retrying...")
            login(keeper_params, login_ui=self)

        sync_down(keeper_params)
        self._keeper_params = keeper_params
        return keeper_params

    def on_device_approval(self, step):
        """Handle device approval automatically using TOTP 2FA code.

        Override of the base ConsoleLoginUi method to automatically approve new
        devices using the stored TOTP key instead of requiring manual user interaction.
        Falls back to the parent implementation if automatic approval fails.

        Args:
            step: The device approval step from Keeper's authentication flow.
        """
        try:
            totp_code = self._get_fresh_totp_code()
            step.send_code(login_steps.DeviceApprovalChannel.TwoFactor, totp_code)
        except Exception as e:
            logger.error(f"Failed to automatically approve device with 2FA: {e}")
            super().on_device_approval(step)

    def on_two_factor(self, step):
        """Handle two-factor authentication automatically using TOTP.

        Override of the base ConsoleLoginUi method to automatically handle 2FA
        challenges using the stored TOTP key. Searches for available TOTP channels
        and automatically provides the current TOTP code.

        Args:
            step: The two-factor authentication step from Keeper's login flow.

        Raises:
            KeeperApiError: If 2FA verification fails or no TOTP channel is available.
        """
        channels = step.get_channels()

        # Find TOTP channel
        totp_channel = None
        totp_ix = 0
        for i, channel in enumerate(channels):
            if "TOTP" in self.two_factor_channel_to_desc(channel.channel_type):
                totp_ix = i
                totp_channel = channel
                break

        if totp_channel is None:
            super().on_two_factor(step)
            return

        channel = channels[totp_ix]

        try:
            totp_code = self._get_fresh_totp_code()
            step.duration = step.get_max_duration()
            step.send_code(channel.channel_uid, totp_code)
        except KeeperApiError as e:
            logger.error(f"Unable to verify Keeper 2FA code: {e}")
            raise e

    def get_all_records(self, record_type: Type[TKeeperRecord] | None = None) -> list[TKeeperRecord]:
        """Retrieve all records from the Keeper vault.

        Fetches all records from the authenticated Keeper vault and optionally
        filters them by record type. Records are loaded from the vault data
        that was synchronized during login.

        Args:
            record_type (Type[TKeeperRecord], optional): The specific type of record
                to filter for. If None, returns all record types. Available record
                types can be found in the keepercommander.vault module.

        Returns:
            list[TKeeperRecord]: A list of Keeper records matching the specified
                                type filter, or all records if no filter is applied.

        Example:
            # Get all records
            all_records = keeper.get_all_records()

            # Get only login records
            from keepercommander.vault import PasswordRecord
            login_records = keeper.get_all_records(PasswordRecord)
        """
        result = [
            KeeperRecord.load(self.keeper_params, record_data)
            for _, record_data in self.keeper_params.record_cache.items()
        ]
        if record_type:
            result = [record for record in result if isinstance(record, record_type)]
        return result

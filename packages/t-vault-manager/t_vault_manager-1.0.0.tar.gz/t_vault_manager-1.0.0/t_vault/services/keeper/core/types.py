"""Types for the keeper service."""

from typing import TypeVar

from keepercommander.vault import KeeperRecord

TKeeperRecord = TypeVar("TKeeperRecord", bound=KeeperRecord)

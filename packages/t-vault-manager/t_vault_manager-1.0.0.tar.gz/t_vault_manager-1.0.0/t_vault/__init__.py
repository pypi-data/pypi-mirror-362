"""Top-level package for T-Bitwarden."""

__author__ = """Thoughtful"""
__email__ = "support@thoughtful.ai"
__version__ = "__version__ = '1.0.0'"

from .t_vault import (
    bw_login,
    bw_get_item,
    bw_login_from_env,
    bw_get_attachment,
    bw_update_password,
    bw_set_default_collection,
    bw_load_collection_items,
    Bitwarden,
    bw_update_custom_fields,
    keeper_login,
    keeper_get_all_records,
    Keeper,
)


__all__ = [
    "bw_login",
    "bw_get_item",
    "bw_login_from_env",
    "bw_get_attachment",
    "bw_update_password",
    "bw_update_custom_fields",
    "keeper_login",
    "keeper_get_all_records",
    "Keeper",
    "bw_set_default_collection",
    "bw_load_collection_items",
    "Bitwarden",
]

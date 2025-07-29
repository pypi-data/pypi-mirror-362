"""Main module."""

from .services.bitwarden import Bitwarden
from .services.keeper import Keeper

# Bitwarden globals
__bw = Bitwarden()
bw_login = __bw.login
bw_login_from_env = __bw.login_from_env
bw_set_default_collection = __bw.set_default_collection
bw_load_collection_items = __bw.load_collection_items
bw_get_item = __bw.get_item
bw_get_attachment = __bw.get_attachment
bw_update_password = __bw.update_password
bw_update_custom_fields = __bw.update_custom_fields

# Keeper globals
__keeper = Keeper()
keeper_login = __keeper.login
keeper_get_all_records = __keeper.get_all_records

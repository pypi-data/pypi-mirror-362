from atexit import register
from difflib import get_close_matches
from os import environ
from subprocess import Popen, run
from time import sleep, time
from typing import Dict, List, Optional

from requests import HTTPError, RequestException, Response, get, post
from retry import retry

from ...models.bitwarden import Attachment, BitWardenItem, VaultItem
from ...models.bitwarden.exceptions import VaultError, VaultItemError, VaultItemNotFoundError
from ...utils.core import BW_PORT, singleton
from ...utils.core.download_bitwarden import get_bw_path, install_bitwarden, is_bitwarden_installed
from ...utils.services import logger


@singleton
class Bitwarden:
    """Bitwarden class."""

    def __init__(self):
        """Initialize the Bitwarden class."""
        if is_bitwarden_installed():
            self.bw_path = get_bw_path()
        else:
            self.bw_path = install_bitwarden()
        self.bw_url = f"http://localhost:{BW_PORT}"

        # In-memory caches: items by ID and name index
        self.vault_items_by_id: Dict[str, VaultItem] = {}
        self._name_index: Dict[str, List[str]] = {}

        # Default collection scope
        self.default_collection: Optional[str] = None

        self.bw_process: Optional[Popen] = None
        register(self.cleanup)

        self.os_env = environ.copy()
        self.password = ""

        self._collection_id_cache: dict[str, str] = {}

    def set_default_collection(self, collection_name: str) -> None:
        """Define a default collection and preload its items into cache."""
        if not collection_name.strip():
            raise VaultError("Collection name must be a non-empty string.")

        # Validate collection name exists by triggering _get_collection_id_by_name;
        # the expected side effect is that it raises an error if the collection does not exist
        _ = self._get_collection_id_by_name(collection_name)

        logger.info(f"Setting default collection to '{collection_name}'.")
        self.default_collection = collection_name

    def cleanup(self) -> None:
        """Clean up resources by terminating the Bitwarden process."""
        try:
            if self.bw_process is not None:
                self.bw_process.terminate()
                self.bw_process.wait(timeout=5)
                self.bw_process = None
        except Exception as e:
            logger.warning(f"Exception during cleanup: {e}")

    def __logout(self) -> None:
        """Logs out the user from the vault."""
        self.cleanup()
        run(
            [self.bw_path, "logout"],
            capture_output=True,
            text=True,
            timeout=180,
            env=self.os_env,
        )

    def _wait_for_server(self, timeout: int = 30, interval: float = 0.5):
        logger.info("Waiting for Bitwarden server to start")
        start_time = time()
        while time() - start_time < timeout:
            try:
                resp = get(f"{self.bw_url}/status", timeout=1)
                if resp.ok:
                    return
            except RequestException:
                pass
            sleep(interval)
        raise VaultError("Bitwarden server failed to start within timeout period")

    @retry(tries=3, delay=5, logger=logger)
    def login_from_env(self, force_latest: bool = False, load_items: bool = True) -> None:
        """Login using environment variables; optionally preload items."""
        if force_latest:
            logger.info("Downloading the latest Bitwarden binary.")
            self.cleanup()
            install_bitwarden(force_latest)

        logger.info("Logging in to Bitwarden.")
        self.__logout()

        MANDATORY_ENV_VARS = [
            "BW_CLIENTID",
            "BW_CLIENTSECRET",
            "BW_PASSWORD",
        ]

        missing_vars = [key for key in MANDATORY_ENV_VARS if key not in self.os_env]

        if missing_vars:
            raise VaultError(f"Environment variable(s) not set: {', '.join(missing_vars)}")

        proc = run(
            [self.bw_path, "login", "--apikey"],
            capture_output=True,
            text=True,
            timeout=30,
            env=self.os_env,
        )
        if proc.returncode != 0:
            raise VaultError(f"Failed to login: {proc.stderr}")

        self.password = self.os_env["BW_PASSWORD"]
        self.open_bw_server()
        self._wait_for_server()
        self.unlock()

        if load_items:
            self._load_all_items()

        if not self.is_vault_unlocked:
            raise VaultError("Failed to unlock the vault. Is the password correct?")

        if load_items and not self.vault_items_by_id:
            logger.warning("No items found in the vault. Re-downloading the binary...")
            self.cleanup()
            install_bitwarden(force_latest)
            raise VaultError("Failed to initialize the vault: No items found.")

    def login(
        self,
        client_id: str,
        client_secret: str,
        password: str,
        username: str = "",
        force_latest: bool = False,
    ) -> None:
        """Login using client credentials and master password."""
        self.os_env["BW_CLIENTID"] = client_id
        self.os_env["BW_CLIENTSECRET"] = client_secret
        self.os_env["BW_PASSWORD"] = password
        self.os_env["BW_USERNAME"] = username
        self.login_from_env(force_latest=force_latest)

    def open_bw_server(self) -> None:
        """Open the Bitwarden server."""
        self.bw_process = Popen(
            [self.bw_path, "serve", "--port", str(BW_PORT)],
            env=self.os_env,
        )

    @retry(tries=5, delay=5)
    def unlock(self) -> None:
        """Unlock the vault."""
        r = post(
            f"{self.bw_url}/unlock",
            json={"password": self.password},
            timeout=5,
        )
        if not r.ok or r.json().get("success") is not True:
            raise VaultError("Failed to unlock vault.")

    def __create_vault_item(self, data: dict) -> VaultItem:
        """Create a VaultItem from raw data."""
        item = BitWardenItem()
        item.name = data.get("name")
        item.totp_key = data.get("login", {}).get("totp")
        item.fields = {f.get("name"): f.get("value") for f in data.get("fields", []) if f.get("name")}
        uris = data.get("login", {}).get("uris") or []
        item.url_list = [u.get("uri") for u in uris if u.get("uri")]
        item.url = item.url_list[0] if item.url_list else None
        item.username = data.get("login", {}).get("username")
        item.password = data.get("login", {}).get("password")
        item.attachments = [
            Attachment(name=a.get("fileName"), item_id=a.get("id"), url=a.get("url"))
            for a in data.get("attachments", [])
            if a.get("fileName")
        ]
        item.collection_id_list = data.get("collectionIds", [])
        item.item_id = data.get("id")
        item.folder_id = data.get("folderId")
        item.notes = data.get("notes")
        return item

    def _load_all_items(self) -> None:
        """Get all items from the vault and index them."""
        logger.info("Loading items from the vault.")
        try:
            r = self._load_all_items_request()
        except RequestException:
            logger.warning("Failed to retrieve all items; will fetch individually on demand")
            return

        if not r.ok:
            raise VaultError("Failed to retrieve items.")

        items = r.json().get("data", {}).get("data", [])
        self._process_items_response(items)

    def load_collection_items(self, collection_name: Optional[str] = None) -> None:
        """Load into cache only the items of the specified (or default) collection."""
        logger.info(f"Loading items from collection {collection_name}.")
        name = collection_name or self.default_collection
        if not name:
            raise VaultError("No default collection defined to load.")
        coll_id = self._get_collection_id_by_name(name)
        # fetch all and filter
        r = self._load_all_items_request()
        r.raise_for_status()
        all_items = r.json().get("data", {}).get("data", [])
        subset = [i for i in all_items if coll_id in i.get("collectionIds", [])]
        self._process_items_response(subset)

    def _process_items_response(self, items: List[dict]) -> None:
        """Index raw item data by ID and build name lookup."""
        self.vault_items_by_id.clear()
        self._name_index.clear()
        for data in items:
            item_id = data.get("id")
            name = data.get("name")
            if not item_id or not name:
                continue
            vault_item = self.__create_vault_item(data)
            self.vault_items_by_id[item_id] = vault_item
            self._name_index.setdefault(name, []).append(item_id)

    def _get_collection_id_by_name(self, collection_name: str) -> str:
        """Look up a collection's ID by its human-friendly name, with caching and fuzzy suggestion."""
        if not hasattr(self, "_collection_id_cache"):
            self._collection_id_cache: dict[str, str] = {}

        if collection_name in self._collection_id_cache:
            return self._collection_id_cache[collection_name]

        # Populate the cache if empty
        try:
            r = get(f"{self.bw_url}/list/object/collections", timeout=30)
            r.raise_for_status()
            collections = r.json().get("data", {}).get("data", [])
            for coll in collections:
                name = coll.get("name")
                coll_id = coll.get("id")
                if name and coll_id:
                    self._collection_id_cache[name] = coll_id
        except RequestException as e:
            raise VaultError(f"Failed to list collections: {e}") from e

        if collection_name not in self._collection_id_cache:
            suggestions = get_close_matches(collection_name, self._collection_id_cache.keys(), n=1)
            suggestion_text = f" Did you mean '{suggestions[0]}'?" if suggestions else ""
            raise VaultError(f"Collection '{collection_name}' does not exist.{suggestion_text}")

        return self._collection_id_cache[collection_name]

    @retry((ConnectionError, HTTPError), tries=7, delay=1, backoff=1)
    def _load_all_items_request(self) -> Response:
        return get(f"{self.bw_url}/list/object/items", timeout=60)

    @retry(exceptions=(RequestException,), tries=3, delay=1)
    def get_item(self, item_name: str, collection_name: Optional[str] = None) -> VaultItem:
        """Get a vault item by name, optionally scoping to a collection or using the default collection."""
        collection_name = collection_name or self.default_collection
        ids = self._name_index.get(item_name, [])

        if not ids:
            # fallback to API
            params = {"search": item_name}
            if collection_name:
                params["collectionId"] = self._get_collection_id_by_name(collection_name)

            r = get(f"{self.bw_url}/list/object/items", params=params, timeout=30)
            if not r.ok:
                raise VaultItemNotFoundError(f"Failed to retrieve item {item_name!r}.")
            data = r.json().get("data", {}).get("data", [])
            if not data:
                raise VaultItemNotFoundError(f"Item {item_name!r} not found.")
            if len(data) > 1:
                raise VaultItemError(f"Multiple items with name {item_name!r} found.")

            vault_item = self.__create_vault_item(data[0])
            self.vault_items_by_id[vault_item.item_id] = vault_item
            self._name_index.setdefault(vault_item.name, []).append(vault_item.item_id)
            return vault_item

        if collection_name is None:
            return self.vault_items_by_id[ids[0]]

        coll_id = self._get_collection_id_by_name(collection_name)
        for item_id in ids:
            item = self.vault_items_by_id[item_id]
            if coll_id in getattr(item, "collection_id_list", []):
                return item

        raise VaultItemNotFoundError(f"Item '{item_name}' not found in collection '{collection_name}'.")

    def get_collection_items(self, collection_name: str) -> List[VaultItem]:
        """Return all items in a given collection."""
        coll_id = self._get_collection_id_by_name(collection_name)
        return [item for item in self.vault_items_by_id.values() if coll_id in getattr(item, "collection_id_list", [])]

    def get_attachment(self, item_name: str, attachment_name: str, file_path: Optional[str] = None) -> str:
        """Get an attachment by name."""
        return self.get_item(item_name).get_attachment(attachment_name, file_path)

    def update_password(self, item_name: str, password: Optional[str] = None) -> str:
        """Update the password of the vault item."""
        return self.get_item(item_name).update_password(password)

    def update_custom_fields(self, item_name: str, fields: dict) -> dict:
        """Update custom fields of the vault item."""
        return self.get_item(item_name).update_custom_fields(fields)

    @property
    def is_vault_unlocked(self) -> bool:
        """Check if the vault is unlocked."""
        if self.bw_process is None:
            return False
        resp = get(f"{self.bw_url}/status", timeout=5)
        if not resp.ok:
            return False
        return resp.json().get("data", {}).get("template", {}).get("status") == "unlocked"

    def __del__(self) -> None:
        """Clean up resources."""
        self.cleanup()

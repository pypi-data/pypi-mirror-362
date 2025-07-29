import difflib

import pytest
import requests

from t_vault import Bitwarden
from t_vault.models.bitwarden.exceptions import VaultError, VaultItemError, VaultItemNotFoundError


class DummyResponse:
    """Simulates the Response object from requests for list/object/items endpoints."""

    def __init__(self, items, ok=True):
        self._items = items
        self.ok = ok

    def json(self):
        return {"data": {"data": self._items}}

    def raise_for_status(self):
        if not self.ok:
            raise requests.HTTPError()


@pytest.fixture(autouse=True)
def clear_vault():
    vault = Bitwarden()
    vault.vault_items_by_id.clear()
    vault._name_index.clear()
    vault.default_collection = None
    if hasattr(vault, "_collection_id_cache"):
        vault._collection_id_cache.clear()
    yield
    vault.vault_items_by_id.clear()
    vault._name_index.clear()
    vault.default_collection = None
    if hasattr(vault, "_collection_id_cache"):
        vault._collection_id_cache.clear()


def make_item(id, name, coll_ids):
    return {
        "id": id,
        "name": name,
        "login": {},
        "fields": [],
        "attachments": [],
        "collectionIds": coll_ids,
        "folderId": None,
        "notes": None,
    }


def test_process_items_response_populates_caches():
    vault = Bitwarden()
    items = [
        make_item("1", "foo", ["c1"]),
        make_item("2", "bar", ["c2"]),
    ]
    vault._process_items_response(items)
    assert set(vault.vault_items_by_id.keys()) == {"1", "2"}
    assert vault._name_index == {"foo": ["1"], "bar": ["2"]}
    vi = vault.vault_items_by_id["1"]
    assert vi.item_id == "1" and vi.name == "foo"


def test_get_item_name_only(monkeypatch):
    vault = Bitwarden()
    vault._process_items_response([make_item("1", "foo", ["c1"])])
    monkeypatch.setattr(
        "t_vault.services.bitwarden.bitwarden.get", lambda *args, **kwargs: DummyResponse(items=[], ok=True)
    )
    monkeypatch.setattr(
        vault, "_get_collection_id_by_name", lambda name: (_ for _ in ()).throw(Exception("Should not be called"))
    )
    item = vault.get_item("foo")
    assert item.item_id == "1"
    with pytest.raises(VaultItemNotFoundError):
        vault.get_item("unknown")


def test_get_item_with_collection(monkeypatch):
    vault = Bitwarden()
    vault._process_items_response(
        [
            make_item("1", "foo", ["c1"]),
            make_item("2", "foo", ["c2"]),
        ]
    )
    monkeypatch.setattr(vault, "_get_collection_id_by_name", lambda name: name)
    it = vault.get_item("foo", collection_name="c2")
    assert it.item_id == "2"
    with pytest.raises(VaultItemNotFoundError):
        vault.get_item("foo", collection_name="does_not_exist")


def test_get_item_filters_by_default_collection(monkeypatch):
    vault = Bitwarden()
    vault._process_items_response(
        [
            make_item("1", "foo", ["c1"]),
            make_item("2", "foo", ["c2"]),
        ]
    )
    vault.default_collection = "c1"
    monkeypatch.setattr(vault, "_get_collection_id_by_name", lambda name: name)
    it = vault.get_item("foo")
    assert it.item_id == "1"


def test_get_collection_items(monkeypatch):
    vault = Bitwarden()
    vault._process_items_response(
        [
            make_item("1", "foo", ["c1"]),
            make_item("2", "bar", ["c1"]),
            make_item("3", "baz", ["c2"]),
        ]
    )
    monkeypatch.setattr(vault, "_get_collection_id_by_name", lambda name: name)
    coll1 = vault.get_collection_items("c1")
    ids = {v.item_id for v in coll1}
    assert ids == {"1", "2"}


def test_load_collection_items(monkeypatch):
    vault = Bitwarden()
    all_items = [
        make_item("1", "foo", ["c1"]),
        make_item("2", "bar", ["c2"]),
        make_item("3", "baz", ["c1", "c2"]),
    ]
    monkeypatch.setattr(vault, "_load_all_items_request", lambda: DummyResponse(all_items))
    monkeypatch.setattr(vault, "_get_collection_id_by_name", lambda name: name)
    vault.load_collection_items("c2")
    assert set(vault.vault_items_by_id.keys()) == {"2", "3"}
    assert vault._name_index["bar"] == ["2"]
    assert vault._name_index["baz"] == ["3"]


def test_set_default_collection_sets_only(monkeypatch):
    vault = Bitwarden()
    monkeypatch.setattr(
        vault, "load_collection_items", lambda name: (_ for _ in ()).throw(Exception("Should not be called"))
    )
    monkeypatch.setattr(vault, "_get_collection_id_by_name", lambda name: name)
    vault.set_default_collection("colX")
    assert vault.default_collection == "colX"


@pytest.mark.parametrize(
    "input_name, expected_suggestion",
    [
        ("NOK health", "Nox Health"),
        ("noxhealth", "Nox Health"),
        ("NoxHealth", "Nox Health"),
        ("Nox  health", "Nox Health"),
    ],
)
def test_set_default_collection_suggests_alternative_on_typo(monkeypatch, input_name, expected_suggestion):
    vault = Bitwarden()
    collections = [
        {"id": "abc", "name": "Financeiro"},
        {"id": "def", "name": "TI"},
        {"id": "xyz", "name": "Nox Health"},
    ]
    monkeypatch.setattr(
        vault,
        "_get_collection_id_by_name",
        lambda name: next(
            (c["id"] for c in collections if c["name"] == name),
            (_ for _ in ()).throw(
                VaultError(
                    f"Collection '{name}' does not exist. Did you mean '{difflib.get_close_matches(name, [c['name'] for c in collections], n=1)[0]}'?"
                )
            ),
        ),
    )
    with pytest.raises(VaultError) as err:
        vault.set_default_collection(input_name)
    assert f"Did you mean '{expected_suggestion}'" in str(err.value)

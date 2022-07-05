from datetime import datetime

from src.stores.entities.store import Store


class TestStore:

    def test_to_dict(self):

        id = 5
        name = "store_example"
        description = "A store to buy a lot of things in mexico"
        warehouse_address = "Yucatan"

        store = Store(id, name, description, warehouse_address)

        dict = store.to_dict()

        assert dict["id"] == id
        assert dict["name"] == name
        assert dict["description"] == description
        assert dict["warehouse_address"] == warehouse_address

    def test_serialize(self):

        id = "1"
        name = "store_example"
        description = "A store to buy a lot of things in mexico"
        warehouse_address = "Yucatan"

        created_at = datetime(year=2021, month=12, day=25,
                              hour=10, minute=24, second=13, microsecond=321654)
        updated_at = datetime(year=2021, month=12, day=25,
                              hour=10, minute=24, second=14, microsecond=321654)
        deleted_at = datetime(year=2021, month=12, day=25,
                              hour=10, minute=24, second=15, microsecond=321654)

        store = Store(
            id=id,
            name=name,
            description=description,
            warehouse_address=warehouse_address,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at
        )

        data = store.serialize()

        assert data["id"] == id
        assert data["name"] == name
        assert data["description"] == description
        assert data["warehouse_address"] == warehouse_address

        assert data["created_at"] == "2021-12-25 10:24:13"
        assert data["updated_at"] == "2021-12-25 10:24:14"

        assert "deleted_at" not in data

    def test_from_dict(self):

        store_dict = {
            "name": "2",
            "description": "test",
            "warehouse_address": "Yucatan"
        }

        store = Store.from_dict(store_dict)

        assert store.name == store_dict["name"]
        assert store.description == store_dict["description"]
        assert store.warehouse_address == store_dict["warehouse_address"]

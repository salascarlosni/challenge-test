from datetime import datetime

from src.products.entities.product import Product


class TestProduct:

    def test_to_dict(self):

        id = 5
        name = "Nintendo switch"
        short_description = "A console to play videogames of nintendo"
        quantity = 5
        store_id = 1

        product = Product(id=id, name=name, store_id=store_id,
                          short_description=short_description, quantity=quantity)

        dict = product.to_dict()

        assert dict["id"] == id
        assert dict["name"] == name
        assert dict["short_description"] == short_description
        assert dict["quantity"] == quantity

    def test_serialize(self):

        id = 5
        name = "Nintendo switch"
        short_description = "A console to play videogames of nintendo"
        quantity = 5
        store_id = 1

        created_at = datetime(year=2021, month=12, day=25,
                              hour=10, minute=24, second=13, microsecond=321654)
        updated_at = datetime(year=2021, month=12, day=25,
                              hour=10, minute=24, second=14, microsecond=321654)
        deleted_at = datetime(year=2021, month=12, day=25,
                              hour=10, minute=24, second=15, microsecond=321654)

        product = Product(
            id=id,
            name=name,
            short_description=short_description,
            quantity=quantity,
            store_id=store_id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at
        )

        data = product.serialize()

        assert data["id"] == id
        assert data["name"] == name
        assert data["short_description"] == short_description
        assert data["quantity"] == quantity

        assert data["created_at"] == "2021-12-25 10:24:13"
        assert data["updated_at"] == "2021-12-25 10:24:14"

        assert "deleted_at" not in data

    def test_from_dict(self):

        product_dict = {
            "name": "Nintendo Switch",
            "short_description": "A console to play videogames of nintendo",
            "quantity": 5,
            "store_id": 1
        }

        product = Product.from_dict(product_dict)

        assert product.name == product_dict["name"]
        assert product.short_description == product_dict["short_description"]
        assert product.quantity == product_dict["quantity"]
        assert product.store_id == product_dict["store_id"]

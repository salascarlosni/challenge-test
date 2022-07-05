from datetime import datetime

from src.orders.entities.order import Order
from src.utils.constants import OrderStatus


class TestOrder:

    def test_to_dict(self):

        id = 5
        status = OrderStatus.CREATED.value
        delivery_address = "Chile"
        user_id = 1

        product = Order(id=id, status=status, user_id=user_id,
                        delivery_address=delivery_address)

        dict = product.to_dict()

        assert dict["id"] == id
        assert dict["status"] == status
        assert dict["delivery_address"] == delivery_address
        assert dict["user_id"] == user_id

    def test_serialize(self):

        id = 5
        status = OrderStatus.CREATED.value
        delivery_address = "Chile"
        user_id = 1

        created_at = datetime(year=2021, month=12, day=25,
                              hour=10, minute=24, second=13, microsecond=321654)
        updated_at = datetime(year=2021, month=12, day=25,
                              hour=10, minute=24, second=14, microsecond=321654)
        deleted_at = datetime(year=2021, month=12, day=25,
                              hour=10, minute=24, second=15, microsecond=321654)

        product = Order(
            id=id,
            status=status,
            delivery_address=delivery_address,
            user_id=user_id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at
        )

        data = product.serialize()

        assert data["id"] == id
        assert data["status"] == status
        assert data["delivery_address"] == delivery_address
        assert data["user_id"] == user_id

        assert data["created_at"] == "2021-12-25 10:24:13"
        assert data["updated_at"] == "2021-12-25 10:24:14"

        assert "deleted_at" not in data

    def test_from_dict(self):

        order_dict = {
            "delivery_address": "A console to play videogames of nintendo",
            "status": OrderStatus.CREATED.value,
            "user_id": 1,
            "id": 1
        }

        product = Order.from_dict(order_dict)

        assert product.id == order_dict["id"]
        assert product.delivery_address == order_dict["delivery_address"]
        assert product.status == order_dict["status"]
        assert product.user_id == order_dict["user_id"]

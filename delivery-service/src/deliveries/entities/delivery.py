from src.utils.utils import format_date
from src.products.entities.product import Product


class Delivery:
    def __init__(
        self,
        id,
        foreign_order_id,
        origin_address,
        customer_name,
        customer_address,
        status,
        created_at=None,
        updated_at=None,
        deleted_at=None,
    ):

        self.id = id
        self.foreign_order_id = foreign_order_id
        self.origin_address = origin_address
        self.customer_name = customer_name
        self.status = status
        self.customer_address = customer_address

        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):
        list_products = []
        for product in self.products:
            list_products.append(Product.serialize(product))

        return {
            "order": {
                "foreign_order_id": self.foreign_order_id,
                "products": list_products,
            },
            "origin": {"address": self.origin_address},
            "destination": {
                "name": self.customer_name,
                "address": self.customer_address,
            },
            "tracking_number": self.id,
            "status": self.status,
        }

    def serialize(self):

        data = self.to_dict()
        return data

    @classmethod
    def from_dict(cls, dict):

        id = dict.get("id")
        foreign_order_id = dict.get("order").get("foreign_order_id")
        origin_address = dict.get("origin").get("address")
        customer_name = dict.get("destination").get("name")
        status = dict.get("status")
        customer_address = dict.get("destination").get("address")

        created_at = dict.get("created_at")
        updated_at = dict.get("updated_at")
        deleted_at = dict.get("deleted_at")

        return Delivery(
            id,
            foreign_order_id,
            origin_address,
            customer_name,
            customer_address,
            status,
            created_at,
            updated_at,
            deleted_at,
        )

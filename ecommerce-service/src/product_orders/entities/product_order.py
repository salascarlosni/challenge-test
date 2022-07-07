from src.utils.utils import format_date


class ProductOrder():

    def __init__(self, id, order_id, quantity, product_id, created_at=None, updated_at=None, deleted_at=None):

        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity

        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):

        return {
            "id": self.id,
            "order_id": self.order_id,
            "quantity": self.quantity,
            "product_id": self.product_id,

            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }

    def serialize(self):

        data = self.to_dict()

        data.pop("deleted_at")

        data["created_at"] = format_date(data["created_at"])
        data["updated_at"] = format_date(data["updated_at"])

        return data

    @classmethod
    def from_dict(cls, dict):

        id = dict.get("id")
        order_id = dict.get("order_id")
        quantity = dict.get("quantity")
        product_id = dict.get("product_id")

        created_at = dict.get("created_at")
        updated_at = dict.get("updated_at")
        deleted_at = dict.get("deleted_at")

        return ProductOrder(
            id=id,
            order_id=order_id,
            quantity=quantity,
            product_id=product_id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at
        )

from src.utils.utils import format_date


class Product:
    def __init__(
        self,
        id,
        sku_id,
        name,
        quantity,
        created_at=None,
        updated_at=None,
        deleted_at=None,
    ):

        self.id = id
        self.sku_id = sku_id
        self.name = name
        self.quantity = quantity

        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):

        return {
            "sku": self.sku_id,
            "name": self.name,
            "qty": self.quantity,
        }

    def serialize(self):

        data = self.to_dict()
        return data

    @classmethod
    def from_dict(cls, dict):

        id = dict.get("id")
        sku_id = dict.get("sku")
        quantity = dict.get("qty")
        name = dict.get("name")

        created_at = dict.get("created_at")
        updated_at = dict.get("updated_at")
        deleted_at = dict.get("deleted_at")

        return Product(
            id,
            sku_id,
            name,
            quantity,
            created_at,
            updated_at,
            deleted_at,
        )

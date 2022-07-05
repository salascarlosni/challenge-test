from src.utils.utils import format_date


class Order():

    def __init__(self, id, status, delivery_address, user_id, created_at=None, updated_at=None, deleted_at=None):

        self.id = id
        self.status = status
        self.delivery_address = delivery_address
        self.user_id = user_id

        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):

        return {
            "id": self.id,
            "status": self.status,
            "delivery_address": self.delivery_address,
            "user_id": self.user_id,

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
        delivery_address = dict.get("delivery_address")
        status = dict.get("status")
        user_id = dict.get("user_id")

        created_at = dict.get("created_at")
        updated_at = dict.get("updated_at")
        deleted_at = dict.get("deleted_at")

        return Order(
            id=id,
            delivery_address=delivery_address,
            user_id=user_id,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at
        )

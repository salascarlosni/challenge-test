from src.utils.utils import format_date


class Tracking:
    def __init__(
        self,
        id,
        status,
        delivery_id,
        created_at=None,
        updated_at=None,
        deleted_at=None,
    ):

        self.id = id
        self.status = status
        self.delivery_id = delivery_id

        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):

        return {
            "status": self.status,
            "date": format_date(self.created_at),
        }

    def serialize(self):

        data = self.to_dict()

        return data

    @classmethod
    def from_dict(cls, dict):

        id = dict.get("id")
        status = dict.get("status")
        delivery_id = dict.get("delivery_id")

        created_at = dict.get("created_at")
        updated_at = dict.get("updated_at")
        deleted_at = dict.get("deleted_at")

        return Tracking(
            id,
            status,
            delivery_id,
            created_at,
            updated_at,
            deleted_at,
        )

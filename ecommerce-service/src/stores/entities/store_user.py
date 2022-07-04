from src.utils.utils import format_date


class StoreUser():

    def __init__(self, user_id, store_id, created_at=None, updated_at=None, deleted_at=None):

        self.user_id = user_id
        self.store_id = store_id

        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):

        return {
            "id": self.id,
            "user_id": self.user_id,
            "store_id": self.store_id,

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

        user_id = dict.get("user_id")
        store_id = dict.get("store_id")

        created_at = dict.get("created_at")
        updated_at = dict.get("updated_at")
        deleted_at = dict.get("deleted_at")

        return StoreUser(user_id, store_id, created_at, updated_at, deleted_at)

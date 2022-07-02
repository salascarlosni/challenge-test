from src.utils.utils import format_date


class User():

    def __init__(
        self,
        id=None, name=None,
        username=None,
        password=None,
        role=None,
        created_at=None,
        updated_at=None,
        deleted_at=None
    ):
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.role = role

        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):

        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,

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
        username = dict.get("username")
        password = dict.get("password")
        name = dict.get("name")

        return User(username=username, password=password, name=name)

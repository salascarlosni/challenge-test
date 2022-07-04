from datetime import datetime

from src.users.entities.user import User
from src.utils.constants import Roles


class TestUser:

    def test_to_dict(self):

        id = 5
        name = "example"
        username = "test@example.com"
        password = "testpassword"
        role = Roles.MARKETPLACE_USER.value

        user = User(id, name, username, password, role)

        dict = user.to_dict()

        assert dict["id"] == id
        assert dict["username"] == username
        assert dict["role"] == role
        assert dict["name"] == name

    def test_serialize(self):

        id = "1"
        username = "test@example.com"
        name = "name"
        role = Roles.MARKETPLACE_ADMIN.value
        shipping_address = "Nicaragua"
        created_at = datetime(year=2021, month=12, day=25,
                              hour=10, minute=24, second=13, microsecond=321654)
        updated_at = datetime(year=2021, month=12, day=25,
                              hour=10, minute=24, second=14, microsecond=321654)
        deleted_at = datetime(year=2021, month=12, day=25,
                              hour=10, minute=24, second=15, microsecond=321654)

        user = User(
            id=id,
            username=username,
            name=name,
            role=role,
            shipping_address=shipping_address,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at
        )

        data = user.serialize()

        assert data["id"] == id
        assert data["username"] == username
        assert data["name"] == name
        assert data["role"] == role
        assert data["created_at"] == "2021-12-25 10:24:13"
        assert data["updated_at"] == "2021-12-25 10:24:14"
        assert data["shipping_address"] == shipping_address

        assert "deleted_at" not in data
        assert "password" not in data

    def test_from_dict(self):

        user_dict = {
            "username": "2",
            "password": "test",
            "name": "test",
            "shipping_address": "Nicaragua",
            "role": Roles.MARKETPLACE_ADMIN.value
        }

        user = User.from_dict(user_dict)

        assert user.password == user_dict["password"]
        assert user.username == user_dict["username"]
        assert user.name == user_dict["name"]
        assert user.role == user_dict["role"]
        assert user.shipping_address == user_dict["shipping_address"]

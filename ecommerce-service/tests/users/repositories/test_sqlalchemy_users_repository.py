import pytest
import bcrypt

from datetime import datetime

from src.frameworks.db.sqlalchemy import SQLAlchemyClient
from src.users.entities.user import User
from src.users.repositories.sqlalchemy_users_repository import SQLAlchemyUsersRepository

from src.utils.constants import Roles


@pytest.fixture(scope="session")
def client():
    return SQLAlchemyClient()


@pytest.fixture(scope="session")
def repository(client):
    return SQLAlchemyUsersRepository(client, test=True)


@pytest.fixture(autouse=True)
def before_each(repository):

    repository.hard_delete_all_users()
    yield


@pytest.fixture(autouse=True, scope="session")
def before_and_after_all(client, repository):

    client.create_tables()

    yield

    repository.drop_users_table()
    client.dispose_mapper()


class TestSqlAlchemyUsersRepository:
    def fake_user(self):

        id = "1"
        username = "test@example.com"
        name = "name"
        password = "pass"
        role = Roles.MARKETPLACE_ADMIN.value
        shipping_address = "Nicaragua"

        salt = bcrypt.gensalt()
        pass_hash = bcrypt.hashpw(password.encode("utf-8"), salt)

        created_at = datetime(
            year=2021,
            month=12,
            day=25,
            hour=10,
            minute=24,
            second=13,
            microsecond=321654,
        )
        updated_at = datetime(
            year=2021,
            month=12,
            day=25,
            hour=10,
            minute=24,
            second=14,
            microsecond=321654,
        )
        deleted_at = datetime(
            year=2021,
            month=12,
            day=25,
            hour=10,
            minute=24,
            second=15,
            microsecond=321654,
        )

        user = User(
            id=id,
            username=username,
            password=pass_hash,
            name=name,
            role=role,
            shipping_address=shipping_address,
            created_at=created_at,
            updated_at=updated_at,
        )

        return user

    def test_create_and_get_user(self, repository: SQLAlchemyUsersRepository):

        user = self.fake_user()
        user = repository.create_user(user)

        saved_user = repository.get_user_by_id(user.id)

        users = repository.get_users()
        for user in users:
            print(user)

        assert user.id == saved_user.id
        assert user.name == saved_user.name
        assert user.username == saved_user.username
        assert user.role == saved_user.role

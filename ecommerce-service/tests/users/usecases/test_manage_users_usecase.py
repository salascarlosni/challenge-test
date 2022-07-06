import pytest

from flask import Flask
from flask_jwt_extended import JWTManager

from unittest import mock
from unittest.mock import Mock

from src.users.entities.user import User
from src.users.usecases.manage_users_usecase import ManageUsersUsecase
from src.utils.constants import Roles


@pytest.fixture
def repository_mock():
    return Mock()


@pytest.fixture
def manage_users_usecase(repository_mock):
    return ManageUsersUsecase(repository_mock)


class TestManageBooksUsecase:

    def test_get_users(self, manage_users_usecase: ManageUsersUsecase):
        mock_users = [
            User(1, "User 1", "test1@example.com", "Nicaragua",
                 "pass1", Roles.MARKETPLACE_ADMIN.value),
            User(2, "User 2", "test2@example.com", "Nicaragua",
                 "pass2", Roles.MARKETPLACE_USER.value),
        ]

        manage_users_usecase.users_repository.get_users.return_value = mock_users
        users = manage_users_usecase.get_users()

        assert len(users) == len(mock_users)
        assert users == mock_users

    @mock.patch('src.utils.get_jwt_token.get_token', return_value="token_test")
    def test_sign_in(self, manage_users_usecase: ManageUsersUsecase):

        manage_users_usecase.users_repository.get_user_by_username_and_password.return_value = User(
            username="test@example.com",
            role=Roles.MARKETPLACE_ADMIN.value
        )

        access_token = manage_users_usecase.sign_in(
            username="test@example.com",
            password="password"
        )

        assert access_token is not None

    @mock.patch('src.utils.get_jwt_token.get_token', return_value="token_test")
    def test_sign_up(self, manage_users_usecase: ManageUsersUsecase):

        manage_users_usecase.users_repository.create_user.return_value = User(
            username="test@example.com",
            role=Roles.MARKETPLACE_ADMIN.value
        )

        access_token = manage_users_usecase.sign_up(
            username="test@example.com",
            name="testing-user",
            password="password",
            shipping_address="Nicaragua"
        )

        assert access_token is not None

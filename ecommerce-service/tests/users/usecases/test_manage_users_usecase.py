import pytest

from datetime import datetime
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

        # Definir que el mock del repositorio retorne tres libros.

        mock_users = [
            User(1, "User 1", "test1@example.com", "pass1", Roles.MARKETPLACE_ADMIN.value),
            User(2, "User 2", "test2@example.com", "pass2", Roles.MARKETPLACE_USER.value),
        ]

        manage_users_usecase.users_repository.get_users.return_value = mock_users

        # Obtener los libros desde el caso de uso, y afirmar que se haya
        # retornado la cantidad correcta de libros.

        users = manage_users_usecase.get_users()
        
        assert len(users) == len(mock_users)
        assert users == mock_users
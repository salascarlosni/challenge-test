import pytest

from unittest.mock import Mock

from src.stores.entities.store import Store
from src.stores.usecases.manage_stores_usecase import ManageStoresUsecase


@pytest.fixture
def repository_mock():
    return Mock()


@pytest.fixture
def manage_stores_usecase(repository_mock):
    return ManageStoresUsecase(repository_mock)


class TestManageStoresUsecase:

    def test_get_stores(self, manage_stores_usecase: ManageStoresUsecase):
        mock_stores = [
            Store(1, "Store 1", "Store1 description example"),
            Store(2, "Store 2", "Store2 description example"),
        ]

        manage_stores_usecase.stores_repository.get_stores.return_value = mock_stores

        stores = manage_stores_usecase.get_stores()

        assert len(stores) == len(mock_stores)

    def test_get_store(self, manage_stores_usecase: ManageStoresUsecase):
        store_id = 1
        mock_store = Store(store_id, "Store 1", "Store1 description example")

        manage_stores_usecase.stores_repository.get_store.return_value = mock_store
        stores = manage_stores_usecase.get_store(store_id)

        assert stores == mock_store

    def test_delete_store(self, manage_stores_usecase: ManageStoresUsecase):
        store_id = 1
        mock_store = Store(store_id, "Store 1", "Store1 description example")

        manage_stores_usecase.stores_repository.update_store.return_value = mock_store
        manage_stores_usecase.stores_repository.get_store.return_value = mock_store

        store = manage_stores_usecase.delete_store(store_id)

        assert store == mock_store

    def test_create_store(self, manage_stores_usecase: ManageStoresUsecase):

        data = {
            "name": "test-store",
            "description": "test-description store",
            "users_ids": [1]
        }

        mock_store = Store.from_dict(data)

        manage_stores_usecase.stores_repository.add_store.return_value = mock_store

        store = manage_stores_usecase.add_store(data)

        assert store.name == data["name"]
        assert store.description == data["description"]

from typing import List
from src.stores.entities.store import Store
from src.utils import utils
from src.stores.repositories.sqlalchemy_store_repository import SQLAlchemyStoresRepository


class ManageStoresUsecase:

    def __init__(self, stores_repository: SQLAlchemyStoresRepository):
        self.stores_repository = stores_repository

    def get_stores(self, name=None) -> List[Store]:
        return self.stores_repository.get_stores(name)

    def get_store(self, id: int) -> Store:
        return self.stores_repository.get_store(id)

    def add_store(self, data) -> Store:
        current_time = utils.get_current_datetime()

        data["created_at"] = current_time
        data["updated_at"] = current_time

        store = Store.from_dict(data)
        users_ids = data["users_ids"]

        store = self.stores_repository.add_store(store, users_ids)

        return store

    def update_store(self, store_id: int, data) -> Store:
        store = self.stores_repository.get_store(store_id)

        if store:
            return self.stores_repository.update_store(store_id, data)
        else:
            raise ValueError(
                f"Store of ID {store_id} doesn't exist or is already deleted.")

    def delete_store(self, store_id: int) -> Store:
        store = self.get_store(store_id)

        if store:

            data = {
                "deleted_at": utils.get_current_datetime()
            }

            store = self.stores_repository.update_store(store_id, data)

        else:
            raise ValueError(
                f"Store of ID {store_id} doesn't exist or is already deleted.")

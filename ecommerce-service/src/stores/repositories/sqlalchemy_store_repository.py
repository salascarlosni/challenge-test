from typing import List
from sqlalchemy import ForeignKey, Table, Column, Integer, String, TIMESTAMP, exc
from sqlalchemy.orm import relationship

from src.frameworks.db.sqlalchemy import SQLAlchemyClient

from src.stores.entities.store import Store
from src.stores.entities.store_user import StoreUser

from src.users.entities.user import User


class SQLAlchemyStoresRepository():

    def __init__(self, sqlalchemy_client: SQLAlchemyClient, test=False):

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "Stores"

        table_name_store_users = "Stores_Users"
        table_name_users = "Users"

        if test:
            table_name += "_test"
            table_name_store_users += "_test"
            table_name_users += "_test"

        self.store_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(50)),
            Column("description", String(200)),
            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),
        )

        self.store_table.users = relationship(
            table_name_users, secondary=table_name_store_users
        )

        # Tabla muchos a muchos que representa los usuarios de una tienda
        self.store_users_table = Table(
            table_name_store_users,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("user_id", ForeignKey(f"{table_name_users}.id")),
            Column("store_id", ForeignKey(f"{table_name}.id")),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(
            Store, self.store_table, properties={
                'users': relationship(
                    User, secondary=table_name_store_users
                )
            }
        )

        sqlalchemy_client.mapper_registry.map_imperatively(
            StoreUser, self.store_users_table
        )

    def get_stores(self, name=None):
        with self.session_factory() as session:
            books_query = session.query(Store).filter_by(deleted_at=None)

            if name:
                books_query.filter_by(Store.name.ilike(f'%{name}%'))

            return books_query.all()

    def add_store(self, store, users_ids):
        with self.session_factory() as session:
            try:
                session.add(store)

                # add users to this store
                for user_id in users_ids:
                    session.execute(self.store_users_table.insert(), params={
                        "user_id": user_id, "store_id": store.id
                    })

                session.commit()
            except exc.IntegrityError:
                session.rollback()
                raise ValueError(
                    "One of the users assigned to this store doesn't exist"
                )

            return store

    def update_store(self, store_id, fields):
        with self.session_factory() as session:
            session.query(Store).filter_by(
                id=store_id, deleted_at=None).update(fields)
            session.commit()

        return self.get_store(store_id)

    def get_store(self, id: int):
        with self.session_factory() as session:
            store = session.query(Store).filter_by(
                id=id, deleted_at=None
            ).first()
            return store

    def hard_delete_store(self, id: int):
        with self.session_factory() as session:
            store = session.query(Store).get(id)
            session.delete(store)
            session.commit()

    def hard_delete_all_stores(self):
        if self.test:
            with self.session_factory() as session:
                session.query(Store).delete()
                session.commit()

    def drop_stores_table(self):
        if self.test:
            self.client.drop_table(self.stores_table)

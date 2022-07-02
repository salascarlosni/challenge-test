import os
import bcrypt

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP
from src.users.entities.user import User

PW_HASH = os.environ["ECOMMERCE_PASS_HASH"]


class SQLAlchemyUsersRepository():

    def __init__(self, sqlalchemy_client, test=False):

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "Users"

        if test:
            table_name += "_test"

        self.users_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("username", String(50)),
            Column("password", String(50)),
            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(
            User, self.users_table)

    def get_users(self):
        with self.session_factory() as session:
            users = session.query(User).filter_by(deleted_at=None).all()

            return users

    def get_user_by_id(self, id):
        with self.session_factory() as session:
            user = session.query(User).filter_by(
                id=id,
                deleted_at=None
            ).first()
            return user

    def create_user(self, user):
        with self.session_factory() as session:
            session.add(user)
            session.commit()

            return user

    def get_user_by_username_and_password(self, username: str, password: str) -> User:
        with self.session_factory() as session:
            user: User = session.query(User).filter_by(
                username=username,
                deleted_at=None
            ).first()

            if user and bcrypt.checkpw(password, user.password):
                return user
            else:
                return None

    def hard_delete_user(self, id: int):
        with self.session_factory() as session:
            user = session.query(User).get(id)
            session.delete(user)
            session.commit()

    def hard_delete_all_users(self):
        if self.test:
            with self.session_factory() as session:
                session.query(User).delete()
                session.commit()

    def drop_users_table(self):
        if self.test:
            self.client.drop_table(self.users_table)

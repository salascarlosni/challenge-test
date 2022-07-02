import os
import bcrypt
from flask_jwt_extended import create_access_token

from src.users.repositories.sqlalchemy_users_repository import SQLAlchemyUsersRepository

PW_HASH = os.environ["ECOMMERCE_PASS_HASH"]


class ManageUsersUsecase:

    def __init__(self, users_repository: SQLAlchemyUsersRepository):
        self.users_repository = users_repository

    def get_users(self):
        return self.users_repository.get_users()

    def sign_up(self, username: str, name: str, password: str) -> str:
        pass_hash = bcrypt.hashpw(password, PW_HASH)
        user = self.users_repository.create_user()

    def sign_in(self, username: str, password: str) -> str:
        user = self.users_repository.get_user_by_username_and_password(
            username, password)

        if not user:
            return None

        return self.get_token(user.username, user.role_id)

    def get_token(username: str, role_id: int) -> str:
        payload = {
            "username": username,
            "role": role_id
        }

        access_token = create_access_token(payload)

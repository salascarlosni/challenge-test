import os
import bcrypt

from flask_jwt_extended import create_access_token
from src.utils import utils

from src.users.repositories.sqlalchemy_users_repository import SQLAlchemyUsersRepository
from src.users.entities.user import User
from src.utils.constants import Roles
from src.utils.get_jwt_token import get_token


class ManageUsersUsecase:

    def __init__(self, users_repository: SQLAlchemyUsersRepository):
        self.users_repository = users_repository

    def get_users(self):
        return self.users_repository.get_users()

    def sign_up(self, username: str, name: str, password: str, role: str = Roles.MARKETPLACE_USER.value) -> str:
        # Register a Internet user as a marketplace user

        salt = bcrypt.gensalt()
        pass_hash = bcrypt.hashpw(password.encode("utf-8"), salt)

        current_time = utils.get_current_datetime()

        user_data = User(
            username=username,
            password=pass_hash,
            name=name,
            created_at=current_time,
            updated_at=current_time,
            role=role
        )

        user = self.users_repository.create_user(user_data)

        if not user:
            return None

        return get_token(user.username, user.role)

    def sign_in(self, username: str, password: str) -> str:
        user = self.users_repository.get_user_by_username_and_password(
            username, password
        )

        if not user:
            return None

        return get_token(user.username, user.role)

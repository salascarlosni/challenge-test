from flask import Blueprint
from flask_jwt_extended import create_access_token


def create_user_blueprint():

    blueprint = Blueprint("users", __name__)

    @blueprint.cli.command("mock-users")
    def mock_users():
        access_token = create_access_token(identity="ADMIN")
        print(access_token)

        return access_token

    return blueprint

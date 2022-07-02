from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from enviame.inputvalidation import validate_schema_flask, FAIL_CODE, SUCCESS_CODE
from src.users.entities.user import User
from src.users.usecases.manage_users_usecase import ManageUsersUsecase

from src.users.http.validation.user_validate_fields import (
    SIGNIN_USER_VALIDATE_FIELDS, SIGNUP_USER_VALIDATE_FIELDS
)


def create_user_blueprint(manage_users_usecase: ManageUsersUsecase):

    blueprint = Blueprint("users", __name__)

    @blueprint.get("/users")
    @jwt_required()
    def list_users():
        return manage_users_usecase.get_users()

    @blueprint.post("/signup")
    @validate_schema_flask(SIGNUP_USER_VALIDATE_FIELDS)
    def sign_up_user():
        body = request.get_json()
        user = User.from_dict(body)

        access_token = manage_users_usecase.sign_in(
            user.username, user.password)

        if access_token:
            code = SUCCESS_CODE
            http_code = 200
            data = access_token
            message = "User sign in succesfully"
        else:
            data = None
            code = FAIL_CODE
            http_code = 401
            message = "Login Failed: Your user ID or password is incorrect"

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = access_token

        return response, http_code

    @blueprint.post('/signin')
    @validate_schema_flask(SIGNIN_USER_VALIDATE_FIELDS)
    def sign_in_user():
        body = request.get_json()
        user = User.from_dict(body)

        access_token = manage_users_usecase.sign_in(
            user.username, user.password)

        if access_token:
            code = SUCCESS_CODE
            http_code = 200
            data = access_token
            message = "User sign in succesfully"
        else:
            data = None
            code = FAIL_CODE
            http_code = 401
            message = "Login Failed: Your user ID or password is incorrect"

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = access_token

        return response, http_code

    return blueprint

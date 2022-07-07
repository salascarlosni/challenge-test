from http import HTTPStatus
import os
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from enviame.inputvalidation import validate_schema_flask, FAIL_CODE, SUCCESS_CODE
from src.users.entities.user import User
from src.users.usecases.manage_users_usecase import ManageUsersUsecase

from src.users.http.validation.user_validate_fields import (
    SIGNIN_USER_VALIDATE_FIELDS,
    SIGNUP_USER_VALIDATE_FIELDS,
)


def create_user_blueprint(manage_users_usecase: ManageUsersUsecase):

    blueprint = Blueprint("users", __name__)

    @blueprint.get("/users")
    @jwt_required()
    def list_users():
        users = manage_users_usecase.get_users()

        users_dict = []
        for user in users:
            users_dict.append(user.serialize())

        response = {
            "code": SUCCESS_CODE,
            "message": "Users obtained succesfully",
            "data": users_dict,
        }

        return response, HTTPStatus.OK

    @blueprint.post("/signup")
    @validate_schema_flask(SIGNUP_USER_VALIDATE_FIELDS)
    def sign_up_user():
        body = request.get_json()
        user = User.from_dict(body)

        access_token = manage_users_usecase.sign_up(
            name=user.name,
            username=user.username,
            password=user.password,
        )

        if access_token:
            code = SUCCESS_CODE
            http_code = 200
            data = access_token
            message = "User sign up succesfully"
        else:
            data = None
            code = FAIL_CODE
            http_code = 401
            message = "Sign up Failed: please try again"

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = access_token

        return response, http_code

    @blueprint.post("/signin")
    @validate_schema_flask(SIGNIN_USER_VALIDATE_FIELDS)
    def sign_in_user():
        body = request.get_json()
        user = User.from_dict(body)

        access_token = manage_users_usecase.sign_in(user.username, user.password)

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

    @blueprint.cli.command("mock-users")
    def mock_users():

        DELIVERY_USER = os.environ.get("ECOMMERCE_DELIVERY_USER")
        DELIVERY_PASS = os.environ.get("ECOMMERCE_DELIVERY_PASS")

        access_token_admin = manage_users_usecase.sign_up(
            name="MARKET_ADMIN",
            username=DELIVERY_USER,
            password=DELIVERY_PASS,
        )

        print(f"TOKEN MARKET_ADMIN: {access_token_admin} ")

    return blueprint

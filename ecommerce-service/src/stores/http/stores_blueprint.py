from http import HTTPStatus
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE

from src.stores.entities.store import Store
from src.stores.usecases.manage_stores_usecase import ManageStoresUsecase
from src.stores.http.validation.store_validate_fields import (
    ADD_STORE_VALIDATE_FIELDS, UPDATE_STORE_VALIDATE_FIELDS
)

from src.utils.authorization import authorization
from src.utils.constants import Roles


def create_stores_blueprint(manage_stores_usecase: ManageStoresUsecase):

    blueprint = Blueprint("stores", __name__)

    @blueprint.before_request
    @jwt_required()
    @authorization(only=[Roles.MARKETPLACE_ADMIN.value])
    def before_request():
        """ Protect all the routes in this blueprint """
        pass

    @blueprint.get("/stores")
    def get_stores(name=None):

        stores: list[Store] = manage_stores_usecase.get_stores(name)

        stores_dict = []
        for store in stores:
            stores_dict.append(store.serialize())

        response = {
            "code": SUCCESS_CODE,
            "message": "Stores obtained succesfully",
            "data": stores_dict,
        }

        return response, HTTPStatus.OK

    @blueprint.post("/stores")
    @validate_schema_flask(ADD_STORE_VALIDATE_FIELDS)
    def add_store():
        body = request.get_json()

        try:
            store = manage_stores_usecase.add_store(body)

            data = store.serialize()
            code = SUCCESS_CODE
            message = "Store created succesfully"
            http_code = HTTPStatus.CREATED

        except ValueError as e:
            data = None
            code = FAIL_CODE
            message = str(e)
            http_code = HTTPStatus.BAD_REQUEST

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.put("/stores/<string:store_id>")
    @validate_schema_flask(UPDATE_STORE_VALIDATE_FIELDS)
    def update_store(store_id):

        body = request.get_json()

        try:
            store = manage_stores_usecase.update_store(store_id, body)

            data = store.serialize()
            code = SUCCESS_CODE
            message = "Store updated succesfully"
            http_code = HTTPStatus.CREATED

        except ValueError as e:
            data = None
            code = FAIL_CODE
            message = str(e)
            http_code = HTTPStatus.BAD_REQUEST

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.get("/stores/<string:store_id>")
    def get_store(store_id):

        store = manage_stores_usecase.get_store(store_id)

        if store:
            data = store.serialize()
            code = SUCCESS_CODE
            message = "Store obtained succesfully"
            http_code = HTTPStatus.OK

        else:
            data = None
            code = FAIL_CODE
            message = f"Store of ID {store_id} does not exist."
            http_code = HTTPStatus.NOT_FOUND

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.delete("/stores/<string:store_id>")
    def delete_store(store_id):

        try:
            manage_stores_usecase.delete_store(store_id)
            code = SUCCESS_CODE
            message = f"Store of ID {store_id} deleted succesfully."
            http_code = HTTPStatus.OK

        except ValueError as e:
            code = FAIL_CODE
            message = str(e)
            http_code = HTTPStatus.BAD_REQUEST

        response = {
            "code": code,
            "message": message,
        }

        return response, http_code

    return blueprint

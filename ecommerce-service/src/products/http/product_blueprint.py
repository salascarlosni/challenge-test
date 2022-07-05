from http import HTTPStatus
from flask import Blueprint, request

from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE
from flask_jwt_extended import jwt_required

from src.products.http.validation.product_validate_fields import (
    ADD_PRODUCT_VALIDATE_FIELDS, UPDATE_PRODUCT_VALIDATE_FIELDS
)
from src.utils.authorization import authorization
from src.utils.constants import Roles


def create_products_blueprint(manage_products_usecase):

    blueprint = Blueprint("products", __name__)

    @blueprint.before_request
    @jwt_required()
    @authorization(only=[Roles.MARKETPLACE_ADMIN.value])
    def before_request():
        """ Protect all the routes in this blueprint """
        pass

    @blueprint.get("/products")
    @jwt_required()
    def get_products():

        products = manage_products_usecase.get_products()

        products_dict = []
        for product in products:
            products_dict.append(product.serialize())

        data = products_dict
        code = SUCCESS_CODE
        message = "List of products obtained succesfully"
        http_code = HTTPStatus.OK

        response = {
            "code": code,
            "message": message,
            "data": data,
        }

        return response, http_code

    @blueprint.get("/products/<string:product_id>")
    def get_product(product_id):

        product = manage_products_usecase.get_product(product_id)

        if product:
            data = product.serialize()
            code = SUCCESS_CODE
            message = "Product obtained succesfully"
            http_code = HTTPStatus.OK

        else:
            data = None
            code = FAIL_CODE
            message = f"Product of ID {product_id} does not exist."
            http_code = HTTPStatus.NOT_FOUND

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.post("/products")
    @validate_schema_flask(ADD_PRODUCT_VALIDATE_FIELDS)
    def add_product():

        body = request.get_json()

        try:
            product = manage_products_usecase.add_product(body)
            data = product.serialize()
            code = SUCCESS_CODE
            message = "product created succesfully"
            http_code = HTTPStatus.CREATED

        except ValueError as e:
            data = None
            code = FAIL_CODE
            message = str(e)
            http_code = 400

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.put("/products/<string:product_id>")
    @validate_schema_flask(UPDATE_PRODUCT_VALIDATE_FIELDS)
    def update_product(product_id):

        body = request.get_json()

        try:
            product = manage_products_usecase.update_product(product_id, body)
            data = product.serialize()
            message = "product updated succesfully"
            code = SUCCESS_CODE
            http_code = 200

        except ValueError as e:
            data = None
            code = FAIL_CODE
            message = str(e)
            http_code = 400

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.delete("/products/<string:product_id>")
    def delete_product(product_id):

        try:
            manage_products_usecase.delete_product(product_id)
            code = SUCCESS_CODE
            message = f"product of ID {product_id} deleted succesfully."
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

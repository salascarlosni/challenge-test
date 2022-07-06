from http import HTTPStatus
from flask import Blueprint, request

from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.product_orders.usecases.manage_product_orders_usecase import ManageProductOrdersUsecase

from src.product_orders.http.validations.product_order_validate_fields import (
    ADD_PRODUCT_ORDER_VALIDATE_FIELDS
)


def create_products_order_blueprint(manage_products_orders_usecasse: ManageProductOrdersUsecase):

    blueprint = Blueprint("product_orders", __name__)

    @blueprint.get("/order/<string:order_id>/products")
    @jwt_required()
    def get_products_from_order(order_id):
        current_user = get_jwt_identity()

        try:
            products = manage_products_orders_usecasse.get_products_from_order(
                order_id, current_user
            )

            products_dict = []
            for product in products:
                products_dict.append(product.serialize())

            data = products_dict
            code = SUCCESS_CODE
            message = "List of products obtained succesfully"
            http_code = HTTPStatus.OK

        except ValueError as e:
            data = None
            code = FAIL_CODE
            message = str(e)
            http_code = HTTPStatus.BAD_REQUEST

        response = {
            "code": code,
            "message": message,
        }

        if data is not None:
            response["data"] = data

        return response, http_code

    @blueprint.post("/order/<string:order_id>/products")
    @jwt_required()
    @validate_schema_flask(ADD_PRODUCT_ORDER_VALIDATE_FIELDS)
    def add_product(order_id):
        current_user = get_jwt_identity()

        body = request.get_json()

        body["order_id"] = order_id

        try:
            product = manage_products_orders_usecasse.add_product_to_order(
                body, current_user
            )

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

    @blueprint.delete("/order/<string:order_id>/products/<string:product_order_id>")
    @jwt_required()
    def delete_product(order_id, product_order_id):
        current_user = get_jwt_identity()

        try:
            manage_products_orders_usecasse.delete_products_from_order(
                order_id, product_order_id, current_user
            )

            code = SUCCESS_CODE
            message = f"product of ID {product_order_id} deleted succesfully."
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

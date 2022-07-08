from http import HTTPStatus
from flask import Blueprint, request

from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.orders.http.validation.order_validation_fields import (
    UPDATE_ORDER_VALIDATE_FIELDS,
)
from src.orders.usecases.manage_orders_usecase import ManageOrdersUsecase

from src.orders.entities.order import Order


def create_orders_blueprint(manage_orders_usecase: ManageOrdersUsecase):

    blueprint = Blueprint("orders", __name__)

    @blueprint.get("/orders")
    @jwt_required()
    def get_orders():
        current_user = get_jwt_identity()
        orders: list[Order] = manage_orders_usecase.get_orders(current_user)

        orders_dict = []
        for order in orders:
            orders_dict.append(order.serialize())

        data = orders_dict
        code = SUCCESS_CODE
        message = "Orders obtained succesfully"
        http_code = HTTPStatus.OK

        response = {
            "code": code,
            "message": message,
            "data": data,
        }

        return response, http_code

    @blueprint.get("/orders/<string:order_id>")
    @jwt_required()
    def get_order(order_id):
        current_user = get_jwt_identity()

        order = manage_orders_usecase.get_order(order_id, current_user)

        if order:
            data = order.serialize()
            code = SUCCESS_CODE
            message = "Order obtained succesfully"
            http_code = HTTPStatus.OK

        else:
            data = None
            code = FAIL_CODE
            message = f"Order of ID {order_id} does not exist."
            http_code = HTTPStatus.NOT_FOUND

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.post("/orders")
    @jwt_required()
    def add_order():
        current_user = get_jwt_identity()
        user_id = current_user["id"]

        try:
            order = manage_orders_usecase.add_order(user_id)
            data = order.serialize()
            code = SUCCESS_CODE
            message = "Order created succesfully"
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

    @blueprint.put("/orders/<string:order_id>")
    @validate_schema_flask(UPDATE_ORDER_VALIDATE_FIELDS)
    @jwt_required()
    def update_order(order_id):
        current_user = get_jwt_identity()
        body = request.get_json()

        try:
            order = manage_orders_usecase.update_order(order_id, body, current_user)
            data = order.serialize()
            message = "Order updated succesfully"
            code = SUCCESS_CODE
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

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.delete("/orders/<string:order_id>")
    @jwt_required()
    def delete_order(order_id):

        current_user = get_jwt_identity()

        try:
            manage_orders_usecase.delete_order(order_id, current_user)
            code = SUCCESS_CODE
            message = f"Order of ID {order_id} deleted succesfully."
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

from http import HTTPStatus
from flask import Blueprint, request

from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE
from flask_jwt_extended import jwt_required

from src.deliveries.http.validation.delivery_validate_fields import (
    DELIVERY_CREATION_VALIDATE_FIELDS,
    DELIVERY_HISTORY_VALIDATE_FIELDS,
)

from src.deliveries.usecases.manage_deliveries_repositories import (
    ManageDeliveriesUsecase,
)

from src.trackings.entities.tracking import Tracking


def create_deliveries_blueprint(manage_deliveries_usecase: ManageDeliveriesUsecase):

    blueprint = Blueprint("deliveries", __name__)

    @blueprint.get("/deliveries")
    @jwt_required()
    def get_deliveries():

        deliveries = manage_deliveries_usecase.get_deliveries()

        deliveries_dict = []
        for delivery in deliveries:
            deliveries_dict.append(delivery.serialize())

        data = deliveries_dict
        code = SUCCESS_CODE
        message = "Deliveries obtained succesfully"
        http_code = 200

        response = {
            "code": code,
            "message": message,
            "data": data,
        }

        return response, http_code

    @blueprint.get("/deliveries/<string:delivery_id>")
    @jwt_required()
    def get_delivery(delivery_id):

        delivery = manage_deliveries_usecase.get_delivery(delivery_id)

        if delivery:
            data = delivery.serialize()
            code = SUCCESS_CODE
            message = "Delivery obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = f"Delivery of ID {delivery_id} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.post("/deliveries")
    @validate_schema_flask(DELIVERY_CREATION_VALIDATE_FIELDS)
    @jwt_required()
    def add_delivery():

        body = request.get_json()

        try:
            delivery = manage_deliveries_usecase.add_delivery(body)
            data = delivery.serialize()
            code = SUCCESS_CODE
            message = "Delivery created succesfully"
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

    # TODO: add functionality
    # @blueprint.put("/deliveries/<string:delivery_id>")
    @validate_schema_flask(DELIVERY_CREATION_VALIDATE_FIELDS)
    @jwt_required()
    def update_delivery(delivery_id):

        body = request.get_json()

        try:
            book = manage_deliveries_usecase.update_delivery(delivery_id, body)
            data = book.serialize()
            message = "Delivery updated succesfully"
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

    @blueprint.delete("/deliveries/<string:delivery_id>")
    @jwt_required()
    def delete_delivery(delivery_id):

        try:
            manage_deliveries_usecase.delete_delivery(delivery_id)
            code = SUCCESS_CODE
            message = f"Delivery of ID {delivery_id} deleted succesfully."
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

    @blueprint.get("/deliveries-history")
    @jwt_required()
    @validate_schema_flask(DELIVERY_HISTORY_VALIDATE_FIELDS)
    def get_delivery_history():

        body = request.get_json()
        delivery_id = body.get("tracking_number")

        delivery = manage_deliveries_usecase.get_delivery(delivery_id)

        if delivery:
            data = {"tracking_number": delivery.id, "status": delivery.status}
            list_trackings = []
            for tracking in delivery.trackings:
                list_trackings.append(Tracking.serialize(tracking))

            data["tracking"] = list_trackings

            code = SUCCESS_CODE
            message = "Delivery obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = f"Delivery of ID {delivery_id} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    return blueprint

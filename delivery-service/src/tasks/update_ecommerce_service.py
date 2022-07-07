from http import HTTPStatus
import json
import os
import random
import requests

from src.utils.constants import DeliveryStatus

ECOMMERCE_DELIVERY_USER = os.environ.get("ECOMMERCE_DELIVERY_USER")
ECOMMERCE_DELIVERY_PASS = os.environ.get("ECOMMERCE_DELIVERY_PASS")


def update_status(order_id, new_status):

    # TODO: improve to use a proper account like GS account or JWT
    # Login to the ecommerce service
    data_login = {
        "username": ECOMMERCE_DELIVERY_USER,
        "password": ECOMMERCE_DELIVERY_PASS,
    }

    login_req = requests.post(
        url=f"http://ecommerce-service:8000/signin", json=data_login
    )
    result_login = json.loads(login_req.text)

    if login_req.status_code == HTTPStatus.OK:

        token = result_login["data"]

        # Send the request to modify the status
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "authorization": f"Bearer {token}",
        }

        data_order = {"status": new_status}
        order_req = requests.put(
            f"http://ecommerce-service:8000//orders/{order_id}",
            json=data_order,
            headers=headers,
        )

    else:
        print("Error login in ecomemrce")


def get_new_deliver_status(status: str):

    if status == DeliveryStatus.READY_FOR_PICK_UP.value:
        return DeliveryStatus.AT_ORIGIN.value
    elif status == DeliveryStatus.AT_ORIGIN.value:
        return DeliveryStatus.EN_ROUTE_OF_DELIVERY.value
    elif status == DeliveryStatus.EN_ROUTE_OF_DELIVERY.value:
        return random.choice(
            [DeliveryStatus.NOT_DELIVERED.value, DeliveryStatus.DELIVERED.value]
        )
    elif status == DeliveryStatus.NOT_DELIVERED.value:
        return DeliveryStatus.EN_ROUTE_OF_DELIVERY.value

    return status

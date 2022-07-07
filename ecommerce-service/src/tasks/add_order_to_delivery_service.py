from http import HTTPStatus
import json
import os
import requests

from src.orders.entities.order import Order

DELIVERY_USER = os.environ.get("ECOMMERCE_DELIVERY_USER")
DELIVERY_PASS = os.environ.get("ECOMMERCE_DELIVERY_PASS")


def update_status(order: Order):

    # Login to the ecommerce service
    data_login = {
        "username": DELIVERY_USER,
        "password": DELIVERY_PASS,
    }

    login_req = requests.post(
        url=f"http://delivery-service:8000/signin", json=data_login
    )
    result_login = json.loads(login_req.text)

    if login_req.status_code == HTTPStatus.OK:

        token = result_login["data"]

        # Send the request to modify the status
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "authorization": f"Bearer {token}",
        }

        data_order = order.serialize_to_delivery()

        order_req = requests.post(
            f"http://delivery-service:8000/deliveries",
            json=data_order,
            headers=headers,
        )

        if order_req.status_code != HTTPStatus.OK:
            print(order_req.status_code)
            print(json.loads(order_req.text))

    else:
        print("Error login in ecomemrce")
        print(result_login)

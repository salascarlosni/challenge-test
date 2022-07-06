ADD_PRODUCT_ORDER_VALIDATE_FIELDS = {
    "product_id": {
        "required": True,
        "type": "integer",
    },

    "quantity": {
        "required": True,
        "type": "integer",
        "min": 1
    },
}

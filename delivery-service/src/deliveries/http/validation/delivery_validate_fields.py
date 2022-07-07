DELIVERY_CREATION_VALIDATE_FIELDS = {
    "order": {
        "type": "dict",
        "schema": {
            "foreign_order_id": {"type": "integer", "required": True},
            "products": {
                "required": True,
                "type": "list",
                "schema": {
                    "required": True,
                    "type": "dict",
                    "empty": False,
                    "schema": {
                        "sku": {
                            "required": True,
                            "type": "integer",
                        },
                        "name": {
                            "required": True,
                            "type": "string",
                        },
                        "qty": {
                            "required": True,
                            "type": "integer",
                        },
                    },
                },
            },
        },
    },
    "origin": {
        "type": "dict",
        "schema": {
            "address": {"type": "string", "required": True},
        },
    },
    "destination": {
        "type": "dict",
        "schema": {
            "name": {"type": "string", "required": True},
            "address": {"type": "string", "required": True},
        },
    },
}

DELIVERY_HISTORY_VALIDATE_FIELDS = {
    "foreing_order_id": {"type": "integer", "required": True},
    "tracking_number": {"type": "integer", "required": True},
}

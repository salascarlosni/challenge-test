ADD_PRODUCT_VALIDATE_FIELDS = {

    "name": {
        "required": True,
        "type": "string",
    },

    "short_description": {
        "required": True,
        "type": "string",
    },

    "quantity": {
        "required": True,
        "type": "integer",
    },

    "store_id": {
        "required": True,
        "type": "integer"
    }

}

UPDATE_PRODUCT_VALIDATE_FIELDS = {

    "name": {
        "required": False,
        "type": "string",
    },

    "short_description": {
        "required": False,
        "type": "string",
    },

    "quantity": {
        "required": False,
        "type": "integer",
    },

}

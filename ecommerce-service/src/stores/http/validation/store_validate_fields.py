ADD_STORE_VALIDATE_FIELDS = {
    "name": {
        "required": True,
        "type": "string",
    },

    "description": {
        "required": True,
        "type": "string"
    },

    "users_ids": {
        "minlength": 1,
        "required": True,
        "type": ["list"],
        "schema": {
            "type": "integer",
        }
    }
}

UPDATE_STORE_VALIDATE_FIELDS = {
    "name": {
        "required": False,
        "type": "string",
    },

    "description": {
        "required": False,
        "type": "string"
    },

    "users_ids": {
        "minlength": 1,
        "required": False,
        "type": ["list"],
        "schema": {
            "type": "integer",
        }
    }
}

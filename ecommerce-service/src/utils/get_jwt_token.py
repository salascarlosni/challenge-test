from flask_jwt_extended import create_access_token


def get_token(username: str, role: str) -> str:
    payload = {
        "username": username,
        "role": role
    }

    access_token = create_access_token(payload)

    return access_token

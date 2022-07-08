from flask_jwt_extended import create_access_token


def get_token(username: str, user_id: int) -> str:
    payload = {"username": username, "id": user_id}

    access_token = create_access_token(payload)

    return access_token

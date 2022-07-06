from flask_jwt_extended import create_access_token


def get_token(username: str, role: str, user_id: int) -> str:
    payload = {
        "username": username,
        "role": role,
        "id": user_id
    }

    access_token = create_access_token(payload)

    return access_token

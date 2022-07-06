from functools import wraps
from http import HTTPStatus
from typing import List

from flask_jwt_extended import get_jwt_identity


def authorization(only: List[str]):
    """ 
    Decorador para validar si un usuario en un rol específico tiene permiso para acceder
    a un endpoint, usarlo junto al decorador de autenticación JWT

    :param only:
        Pasa la lista de roles que tienen permiso de acceder al resource con el decorador asignado

    """

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()

            if not current_user:
                return "User not found", HTTPStatus.UNAUTHORIZED

            role = current_user["role"]

            if role not in only:
                return "You don't have permission to perform this action", HTTPStatus.FORBIDDEN

            retval = function(*args, **kwargs)

            return retval
        return wrapper
    return decorator

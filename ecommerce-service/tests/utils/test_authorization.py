from tests.conftest import create_test_app
from src.utils.get_jwt_token import get_token
from src.utils.constants import Roles

# Tests para las funciones utilitarias de autenticacion.


class TestAuthorization:
    def test_get_jwt_token(self):

        # Mock una app Flask para probar a obtener un jwt key
        with create_test_app().app_context():
            access_token = get_token(
                username="testing@example.com", role=Roles.MARKETPLACE_USER.value, user_id=1
            )

            assert access_token is not None

from datetime import timedelta
import pytest

from flask import Flask
from flask_jwt_extended import JWTManager


def create_test_app():
    app = Flask("testing")
    app.config.update({
        "TESTING": True,
    })
    app.config["JWT_SECRET_KEY"] = "TESTING_KEY"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(milliseconds=1)
    JWTManager(app)

    return app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

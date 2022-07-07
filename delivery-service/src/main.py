import os
from datetime import timedelta
from flask_jwt_extended import JWTManager

from src.frameworks.db.firestore import create_firestore_client
from src.frameworks.db.redis import create_redis_client
from src.frameworks.db.sqlalchemy import SQLAlchemyClient
from src.frameworks.http.flask import create_flask_app

from src.books.http.books_blueprint import create_books_blueprint
from src.books.repositories.firestore_books_repository import FirestoreBooksRepository
from src.books.repositories.sqlalchemy_books_repository import SQLAlchemyBooksRepository
from src.books.usecases.manage_books_usecase import ManageBooksUsecase

from src.greeting.http.greeting_blueprint import create_greeting_blueprint
from src.greeting.repositories.redis_greeting_cache import RedisGreetingCache
from src.greeting.usecases.greeting_usecase import GreetingUsecase

from src.deliveries.repositories.sqlalchemy_deliveries_repository import (
    SQLAlchemyDeliveriesRepository,
)
from src.deliveries.http.delivery_blueprint import create_deliveries_blueprint

from src.deliveries.usecases.manage_deliveries_repositories import (
    ManageDeliveriesUsecase,
)

from src.products.repositories.sqlalchemy_products_repository import (
    SQLAlchemyProductsRepository,
)

from src.trackings.repositories.sqlalchemy_trackings_repository import (
    SQLAlchemyTrackingsRepository,
)

# Instanciar dependencias.

# En el caso de uso de de libros, es es posible pasarle como parámetro el repositorio
# de Firestore o el repositorio con SQL Alchemy, y en ambos casos debería funcionar,
# incluso si el cambio se hace mientras la aplicación está en ejecución.

redis_client = create_redis_client()
redis_greeting_cache = RedisGreetingCache(redis_client)

firestore_client = create_firestore_client()
firestore_books_repository = FirestoreBooksRepository(firestore_client)

sqlalchemy_client = SQLAlchemyClient()
sqlalchemy_books_repository = SQLAlchemyBooksRepository(sqlalchemy_client)
sqlalchemy_deliveries_repository = SQLAlchemyDeliveriesRepository(sqlalchemy_client)
sqlalchemy_products_repository = SQLAlchemyProductsRepository(sqlalchemy_client)
sqlalchemy_trackings_repository = SQLAlchemyTrackingsRepository(sqlalchemy_client)

sqlalchemy_client.create_tables()

greeting_usecase = GreetingUsecase(redis_greeting_cache)
manage_books_usecase = ManageBooksUsecase(firestore_books_repository)
manage_deliveries_usecase = ManageDeliveriesUsecase(sqlalchemy_deliveries_repository)

# manage_books_usecase = ManageBooksUsecase(sqlalchemy_books_repository)

blueprints = [
    create_books_blueprint(manage_books_usecase),
    create_greeting_blueprint(greeting_usecase),
    create_deliveries_blueprint(manage_deliveries_usecase),
]

# Crear aplicación HTTP con dependencias inyectadas.
app = create_flask_app(blueprints)

# Configurando JWT para autenticatión en el microservicio
# TODO: cambiar a un tiempo menor y usar refresh token
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(weeks=4)
JWTManager(app)

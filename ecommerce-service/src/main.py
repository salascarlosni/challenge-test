import os
from flask_jwt_extended import JWTManager

from datetime import timedelta

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

from src.users.http.user_blueprint import create_user_blueprint
from src.users.repositories.sqlalchemy_users_repository import SQLAlchemyUsersRepository
from src.users.usecases.manage_users_usecase import ManageUsersUsecase

from src.stores.http.stores_blueprint import create_stores_blueprint
from src.stores.repositories.sqlalchemy_store_repository import SQLAlchemyStoresRepository
from src.stores.usecases.manage_stores_usecase import ManageStoresUsecase

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
sqlalchemy_users_repository = SQLAlchemyUsersRepository(sqlalchemy_client)
sqlalchemy_stores_repository = SQLAlchemyStoresRepository(sqlalchemy_client)

sqlalchemy_client.create_tables()

# UseCases
greeting_usecase = GreetingUsecase(redis_greeting_cache)
manage_books_usecase = ManageBooksUsecase(sqlalchemy_books_repository)
manage_stores_usecase = ManageStoresUsecase(sqlalchemy_stores_repository)
manage_users_usecase = ManageUsersUsecase(sqlalchemy_users_repository)


blueprints = [
    create_books_blueprint(manage_books_usecase),
    create_greeting_blueprint(greeting_usecase),
    create_user_blueprint(manage_users_usecase),
    create_stores_blueprint(manage_stores_usecase)
]

# Crear aplicación HTTP con dependencias inyectadas.
app = create_flask_app(blueprints)

# Configurando JWT para autenticatión en el microservicio
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(weeks=1)
JWTManager(app)

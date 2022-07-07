from sqlalchemy import ForeignKey, Table, Column, Integer, String, TIMESTAMP
from src.products.entities.product import Product


class SQLAlchemyProductsRepository:
    def __init__(self, sqlalchemy_client, test=False):

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name_deliveries = "Deliveries"
        table_name_products = "Products"

        if test:
            table_name_deliveries += "_test"
            table_name_products += "_test"

        self.products_table = Table(
            table_name_products,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("sku_id", Integer),
            Column("name", String(50)),
            Column("quantity", Integer),
            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),
            # relationships
            Column("delivery_id", Integer, ForeignKey(f"{table_name_deliveries}.id")),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(Product, self.products_table)

    def hard_delete_book(self, id):

        with self.session_factory() as session:

            book = session.query(Product).get(id)
            session.delete(book)
            session.commit()

    def hard_delete_all_books(self):

        if self.test:

            with self.session_factory() as session:

                session.query(Product).delete()
                session.commit()

    def drop_books_table(self):

        if self.test:
            self.client.drop_table(self.products_table)

from sqlalchemy import ForeignKey, Table, Column, Integer, String, TIMESTAMP, exc

from src.frameworks.db.sqlalchemy import SQLAlchemyClient

from src.products.entities.product import Product


class SQLAlchemyProductRepository():

    def __init__(self, sqlalchemy_client: SQLAlchemyClient, test=False):

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "Products"
        table_name_store = "Stores"

        if test:
            table_name += "_test"
            table_name_store += "_test"

        self.products_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(50)),
            Column("short_description", String(200)),
            Column("quantity", Integer),
            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),

            # relationships
            Column("store_id", Integer, ForeignKey(f"{table_name_store}.id"))
        )

        sqlalchemy_client.mapper_registry.map_imperatively(
            Product, self.products_table
        )

    def get_products(self, name=None):
        with self.session_factory() as session:
            products_query = session.query(Product).filter_by(deleted_at=None)

            if name:
                products_query.filter_by(Product.name.ilike(f'%{name}%'))

            return products_query.all()

    def add_product(self, product):
        with self.session_factory() as session:
            try:
                session.add(product)
                session.commit()
            except exc.IntegrityError:
                session.rollback()
                raise ValueError(
                    "the store selected doesn't exist or was deleted"
                )

            return product

    def update_product(self, product_id, fields):
        with self.session_factory() as session:
            session.query(Product).filter_by(
                id=product_id, deleted_at=None
            ).update(fields)
            session.commit()

        return self.get_product(product_id)

    def get_product(self, product_id: int):
        with self.session_factory() as session:
            product = session.query(Product).filter_by(
                id=product_id, deleted_at=None
            ).first()
            return product

    def hard_delete_product(self, product_id: int):
        with self.session_factory() as session:
            product = session.query(Product).get(id=product_id)
            session.delete(product)
            session.commit()

    def hard_delete_all_products(self):
        if self.test:
            with self.session_factory() as session:
                session.query(Product).delete()
                session.commit()

    def drop_products_table(self):
        if self.test:
            self.client.drop_table(self.products_table)

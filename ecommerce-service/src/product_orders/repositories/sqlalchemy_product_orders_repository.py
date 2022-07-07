from sqlalchemy import ForeignKey, Table, Column, Integer, TIMESTAMP, exc
from sqlalchemy.orm import relationship

from src.frameworks.db.sqlalchemy import SQLAlchemyClient

from src.product_orders.entities.product_order import ProductOrder
from src.products.entities.product import Product


class SQLAlchemyProductOrderRepository:
    def __init__(self, sqlalchemy_client: SQLAlchemyClient, test=False):

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "Product_Orders"

        if test:
            table_name += "_test"

        self.product_orders_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("quantity", Integer),
            Column("product_id", ForeignKey("Products.id")),
            Column("order_id", ForeignKey("Orders.id")),
            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(
            ProductOrder,
            self.product_orders_table,
            properties={
                "product": relationship(
                    Product, backref="order_product", lazy="joined"
                ),
            },
        )

    def get_products_from_order(self, order_id):
        with self.session_factory() as session:
            products_query = session.query(ProductOrder).filter_by(
                deleted_at=None, order_id=order_id
            )

            return products_query.all()

    def add_product_to_order(self, order):
        with self.session_factory() as session:
            try:
                session.add(order)
                session.commit()
            except exc.IntegrityError:
                session.rollback()
                raise ValueError("the order selected doesn't exist or was deleted")

            return order

    def delete_product_from_order(self, order):
        with self.session_factory() as session:
            try:
                session.add(order)
                session.commit()
            except exc.IntegrityError:
                session.rollback()
                raise ValueError("the order selected doesn't exist or was deleted")

            return order

    def hard_delete_product_order(self, id):
        with self.session_factory() as session:
            product_order = session.query(ProductOrder).get(id)
            session.delete(product_order)
            session.commit()

            return product_order

    def hard_delete_all_product_orders(self):
        if self.test:
            with self.session_factory() as session:
                session.query(ProductOrder).delete()
                session.commit()

    def drop_product_orders_table(self):
        if self.test:
            self.client.drop_table(self.product_orders_table)

from sqlalchemy import ForeignKey, Table, Column, Integer, String, TIMESTAMP, exc

from src.frameworks.db.sqlalchemy import SQLAlchemyClient

from src.orders.entities.order import Order


class SQLAlchemyOrderRepository():

    def __init__(self, sqlalchemy_client: SQLAlchemyClient, test=False):

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "Orders"
        table_name_users = "Users"

        if test:
            table_name += "_test"
            table_name_users += "_test"

        self.orders_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("status", String(20)),
            Column("delivery_address", String(200)),
            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),

            # relationships
            Column("user_id", Integer, ForeignKey(f"{table_name_users}.id"))
        )

        sqlalchemy_client.mapper_registry.map_imperatively(
            Order, self.orders_table
        )

    def get_orders(self, user_id=None):
        with self.session_factory() as session:
            orders_query = session.query(Order).filter_by(deleted_at=None)

            if user_id:
                orders_query.filter_by(user_id=user_id)

            return orders_query.all()

    def add_order(self, order):
        with self.session_factory() as session:
            try:
                session.add(order)
                session.commit()
            except exc.IntegrityError:
                session.rollback()
                raise ValueError(
                    "the order selected doesn't exist or was deleted"
                )

            return order

    def update_order(self, order_id, fields):
        with self.session_factory() as session:
            session.query(Order).filter_by(
                id=order_id, deleted_at=None
            ).update(fields)
            session.commit()

        return self.get_order(order_id)

    def get_order(self, order_id: int, user_id: int = None):
        with self.session_factory() as session:
            order = session.query(Order).filter_by(
                id=order_id, deleted_at=None
            )

            if user_id:
                order.filter_by(user_id=user_id)

            return order.first()

    def hard_delete_order(self, order_id: int):
        with self.session_factory() as session:
            order = session.query(Order).get(id=order_id)
            session.delete(order)
            session.commit()

    def hard_delete_all_orders(self):
        if self.test:
            with self.session_factory() as session:
                session.query(Order).delete()
                session.commit()

    def drop_orders_table(self):
        if self.test:
            self.client.drop_table(self.orders_table)

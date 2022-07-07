from sqlalchemy import Table, Column, Integer, String, TIMESTAMP

from src.deliveries.entities.delivery import Delivery
from src.products.entities.product import Product
from src.trackings.entities.tracking import Tracking

from sqlalchemy.orm import relationship


class SQLAlchemyDeliveriesRepository:
    def __init__(self, sqlalchemy_client, test=False):

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name_deliveries = "Deliveries"
        table_name_products = "Products"
        table_name_trackings = "Trackings"

        if test:
            table_name_deliveries += "_test"
            table_name_products += "_test"
            table_name_trackings += "_test"

        self.deliveries_table = Table(
            table_name_deliveries,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("foreign_order_id", Integer),
            Column("origin_address", String(200)),
            Column("customer_name", String(100)),
            Column("customer_address", String(200)),
            Column("status", String(20)),
            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(
            Delivery,
            self.deliveries_table,
            properties={
                "trackings": relationship(
                    Tracking, backref="delivery_trackings", lazy="joined"
                ),
                "products": relationship(
                    Product, backref="delivery_products", lazy="joined"
                ),
            },
        )

    def add_delivery(self, delivery):

        with self.session_factory() as session:
            session.add(delivery)
            session.commit()

        return delivery

    def get_deliveries(self):

        with self.session_factory() as session:
            deliveries = session.query(Delivery).filter_by(deleted_at=None).all()

        return deliveries

    def update_delivery(self, delivery_id, fields):

        with self.session_factory() as session:
            session.query(Delivery).filter_by(id=delivery_id, deleted_at=None).update(
                fields
            )
            session.commit()

        return self.get_delivery(delivery_id)

    def get_delivery(self, order_id):

        with self.session_factory() as session:
            shipping_order_detail = (
                session.query(Delivery).filter_by(id=order_id, deleted_at=None).first()
            )

        return shipping_order_detail

    def hard_delete_deliveries(self, id):

        with self.session_factory() as session:
            delivery = session.query(Delivery).get(id)
            session.delete(delivery)
            session.commit()

    def hard_delete_all_deliveries(self):

        if self.test:
            with self.session_factory() as session:

                session.query(Delivery).delete()
                session.commit()

    def drop_deliveries_table(self):

        if self.test:
            self.client.drop_table(self.deliveries_table)

from sqlalchemy import ForeignKey, Table, Column, Integer, String, TIMESTAMP

from src.trackings.entities.tracking import Tracking


class SQLAlchemyTrackingsRepository:
    def __init__(self, sqlalchemy_client, test=False):

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name_deliveries = "Deliveries"
        table_name_trackings = "Trackings"

        if test:
            table_name_deliveries += "_test"
            table_name_trackings += "_test"

        self.tracking_table = Table(
            table_name_trackings,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("status", String(20)),
            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),
            # relationships
            Column("delivery_id", Integer, ForeignKey(f"{table_name_deliveries}.id")),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(
            Tracking, self.tracking_table
        )

    def hard_delete_tracking(self, id):

        with self.session_factory() as session:
            tracking = session.query(Tracking).get(id)
            session.delete(tracking)
            session.commit()

    def hard_delete_all_trakcings(self):

        if self.test:
            with self.session_factory() as session:
                session.query(Tracking).delete()
                session.commit()

    def drop_tracking_table(self):

        if self.test:
            self.client.drop_table(self.tracking_table)

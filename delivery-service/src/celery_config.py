import os
from celery import Celery, shared_task
from celery.utils.log import get_task_logger
from datetime import timedelta

from src.utils.constants import DeliveryStatus
from src.frameworks.db.sqlalchemy import SQLAlchemyClient

from src.deliveries.repositories.sqlalchemy_deliveries_repository import (
    SQLAlchemyDeliveriesRepository,
)

from src.deliveries.usecases.manage_deliveries_repositories import (
    ManageDeliveriesUsecase,
)

from src.tasks.update_ecommerce_service import get_new_deliver_status, update_status

from src.main import manage_deliveries_usecase

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]

logger = get_task_logger(__name__)


celery = Celery(__name__)
celery.conf.broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}"
celery.conf.result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}"

celery.autodiscover_tasks()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls every 30 seconds

    sender.add_periodic_task(
        5.0,
        change_status_of_orders.s(),
        name="Change order delivery",
    )


@celery.task()
def change_status_of_orders():

    deliveries = manage_deliveries_usecase.get_deliveries()

    for delivery in deliveries:
        new_status = get_new_deliver_status(delivery.status)

        # We update the db delivery to the new status
        delivery_updated = manage_deliveries_usecase.update_delivery(
            delivery.id, {"status": new_status}
        )

        if new_status == DeliveryStatus.DELIVERED.value:
            # We call the ecommerce service to finally update the status of this order
            update_status(delivery_updated.foreign_order_id, new_status)

    return "Orders updated succesfully"


# @celery.task
# def testing():
#    print("testing task")

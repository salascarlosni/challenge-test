import os
from celery import Celery, shared_task
from celery.utils.log import get_task_logger
from datetime import timedelta

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]

logger = get_task_logger(__name__)


celery = Celery(__name__)
celery.conf.broker_url =f"redis://{REDIS_HOST}:{REDIS_PORT}"
celery.conf.result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}"

celery.autodiscover_tasks()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls every 30 seconds.
    sender.add_periodic_task(30.0, change_status_of_orders.s(), name="Change order delivery")

@celery.task()
def change_status_of_orders():
    logger.info("run")
    logger.info("The sample task just ran.")
    print("s")
    return "hola"

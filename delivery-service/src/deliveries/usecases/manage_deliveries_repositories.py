from src.utils import utils

from src.deliveries.repositories.sqlalchemy_deliveries_repository import (
    SQLAlchemyDeliveriesRepository,
)

from src.deliveries.entities.delivery import Delivery
from src.products.entities.product import Product
from src.trackings.entities.tracking import Tracking

from src.utils.constants import DeliveryStatus


class ManageDeliveriesUsecase:
    def __init__(self, deliveries_repository: SQLAlchemyDeliveriesRepository):
        self.deliveries_repository = deliveries_repository

    def get_deliveries(self):
        return self.deliveries_repository.get_deliveries()

    def get_delivery(self, delivery_id):
        return self.deliveries_repository.get_delivery(delivery_id)

    def add_delivery(self, data):
        list_products = data.get("order").get("products")
        list_product_models = []

        # Adding timestamps and the status of the delivery
        current_time = utils.get_current_datetime()

        first_tracking_data = {
            "created_at": current_time,
            "status": DeliveryStatus.READY_FOR_PICK_UP.value,
            "updated_at": current_time,
        }

        # Create a delivery object merging the first tracking dict in the data dict provided
        delivery = Delivery.from_dict({**data, **first_tracking_data})

        # Mapping product relationships to the new delivery
        for product in list_products:
            product["created_at"] = current_time
            product["updated_at"] = current_time

            list_product_models.append(Product.from_dict(product))

        delivery.products = list_product_models

        # Map the first tracking status to this delivery
        tracking = Tracking.from_dict(first_tracking_data)
        delivery.trackings = [tracking]

        # Finally we insert the delivery
        delivery_added = self.deliveries_repository.add_delivery(delivery)

        if not delivery_added:
            raise ValueError("Error while creating a new delivery")

        return delivery_added

    def update_delivery(self, delivery_id, data):
        delivery = self.get_delivery(delivery_id)

        if not delivery:
            raise ValueError(
                f"Delivery of ID {delivery_id} doesn't exist or is already deleted."
            )

        # Adding timestamps and the status of the delivery
        current_time = utils.get_current_datetime()

        # Add a new tracking history status to this delivery
        if "status" in data:

            # Validate that the status inserted is existing
            if data["status"] not in DeliveryStatus.__members__:
                raise ValueError(f"Status sent is not valid, please try again")

            first_tracking_data = {
                "created_at": current_time,
                "status": data["status"],
                "updated_at": current_time,
            }

            tracking = Tracking(first_tracking_data)
            tracking_list = delivery.trackings.append(tracking)

            # data["trackings"] = tracking_list

        delivery = self.deliveries_repository.update_delivery(delivery_id, data)

        return delivery

    def delete_delivery(self, delivery_id):
        delivery = self.get_delivery(delivery_id)

        if not delivery:
            raise ValueError(
                f"Delivery of ID {delivery_id} doesn't exist or is already deleted."
            )

        delivery_updated = self.deliveries_repository.update_delivery(
            delivery_id, {"deleted_at": utils.get_current_datetime()}
        )

        return delivery_updated

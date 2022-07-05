from src.utils import utils

from src.orders.entities.order import Order
from src.orders.repositories.sqlalchemy_order_repository import SQLAlchemyOrderRepository
from src.users.repositories.sqlalchemy_users_repository import SQLAlchemyUsersRepository

from src.utils.constants import OrderStatus, Roles


class ManageOrdersUsecase:

    def __init__(self, orders_repository: SQLAlchemyOrderRepository, users_repository: SQLAlchemyUsersRepository):
        self.orders_repository = orders_repository
        self.users_repository = users_repository

    def get_orders(self, current_user):
        # If the user is not an admin, then only show his orders

        if current_user["role"] == Roles.MARKETPLACE_USER.value:
            return self.orders_repository.get_orders(current_user["id"])
        else:
            return self.orders_repository.get_orders()

    def get_order(self, order_id: int, current_user):
        if current_user["role"] == Roles.MARKETPLACE_USER.value:
            return self.orders_repository.get_order(order_id, current_user["id"])
        else:
            return self.orders_repository.get_order(order_id)

    def add_order(self, user_id):

        user = self.users_repository.get_user_by_id(user_id)

        current_time = utils.get_current_datetime()
        data = {
            "created_at": current_time,
            "updated_at": current_time,
            "user_id": user_id,
            "delivery_address": user.shipping_address,
            "status": OrderStatus.PENDING.value
        }

        order = Order.from_dict(data)
        order = self.orders_repository.add_order(order)

        return order

    def update_order(self, order_id, data):

        order = self.get_order(order_id)

        if order:
            data["updated_at"] = utils.get_current_datetime()

            if data["status"] not in OrderStatus.__members__.values():
                raise ValueError(f"Status sent is not valid, please try again")

            order = self.order_repository.update_order(order_id, data)

            return order

        else:
            raise ValueError(f"order of ID {order_id} doesn't exist.")

    def delete_order(self, order_id, current_user):

        order = self.get_order(order_id, current_user)

        if order:

            data = {
                "deleted_at": utils.get_current_datetime()
            }

            order = self.orders_repository.update_order(order_id, data)
            return order

        else:
            raise ValueError(
                f"order of ID {order_id} doesn't exist or is already deleted.")

from src.product_orders.entities.product_order import ProductOrder
from src.product_orders.repositories.sqlalchemy_product_orders_repository import SQLAlchemyProductOrderRepository

from src.orders.repositories.sqlalchemy_order_repository import SQLAlchemyOrderRepository
from src.users.repositories.sqlalchemy_users_repository import SQLAlchemyUsersRepository
from src.product_orders.repositories.sqlalchemy_product_orders_repository import SQLAlchemyProductOrderRepository
from src.products.repositories.sqlalchemy_product_repository import SQLAlchemyProductRepository

from src.utils.constants import Roles
from src.utils import utils


class ManageProductOrdersUsecase:

    def __init__(
        self,
        order_repository: SQLAlchemyOrderRepository,
        product_orders_repository: SQLAlchemyProductOrderRepository,
        product_repository: SQLAlchemyProductRepository,
        users_repository: SQLAlchemyUsersRepository
    ):
        self.product_orders_repository = product_orders_repository
        self.order_repository = order_repository
        self.users_repository = users_repository
        self.product_repository = product_repository

    def get_products_from_order(self, order_id, current_user):
        # If the user is not an admin, then only show his orders

        self.validation_of_order(order_id, current_user)

        return self.product_orders_repository.get_products_from_order(order_id)

    def delete_products_from_order(self, order_id: int, product_order_id: int, current_user):
        order = self.validation_of_order(order_id, current_user)

        order_product = self.product_orders_repository.hard_delete_product_order(
            product_order_id
        )

        # Update stock to add the removed quantity
        if not order:
            raise ValueError(
                "The product selected doesn't exist or was already deleted"
            )

        product_id = order_product.product_id
        product_base = self.product_repository.get_product(product_id)

        new_quantity = product_base.quantity + order_product.quantity
        fields = {"quantity": new_quantity}

        self.product_repository.update_product(product_id, fields)

        return order

    def add_product_to_order(self, data, current_user):

        product_id = data["product_id"]
        order_id = data["order_id"]
        quantity = data["quantity"]

        self.validation_of_order(order_id, current_user)

        product_base = self.product_repository.get_product(product_id)

        if not product_base:
            raise ValueError(
                "The product selected doesn't exist or was already deleted"
            )

        new_quantity = product_base.quantity - quantity

        if new_quantity <= 0:
            raise ValueError(
                "Not enough quantity of this product for order"
            )

        current_time = utils.get_current_datetime()

        data["created_at"] = current_time
        data["updated_at"] = current_time

        order_product = ProductOrder.from_dict(data)

        product_order = self.product_orders_repository.add_product_to_order(
            order_product
        )

        if not product_order:
            raise ValueError(
                "Error while adding this product to the order, please try again"
            )

        fields = {"quantity": new_quantity}
        self.product_repository.update_product(product_id, fields)

        return product_order

    def validation_of_order(self, order_id, current_user):
        "Validar que la orden pertenece a este usuario en caso que no sea admin"

        if current_user["role"] == Roles.MARKETPLACE_USER.value:
            order = self.order_repository.get_order(
                order_id, current_user["id"]
            )

        else:
            order = self.order_repository.get_order(order_id)

        if not order:
            raise ValueError(
                "the order selected doesn't exist or was deleted"
            )

        return order

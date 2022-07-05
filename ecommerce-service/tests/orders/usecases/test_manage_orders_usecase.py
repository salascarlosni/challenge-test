import pytest

from unittest.mock import Mock

from src.orders.entities.order import Order
from src.orders.usecases.manage_orders_usecase import ManageOrdersUsecase
from src.utils.constants import OrderStatus, Roles
from src.users.usecases.manage_users_usecase import ManageUsersUsecase


@pytest.fixture
def order_repository_mock():
    return Mock()


@pytest.fixture
def user_repository_mock():
    return Mock()


@pytest.fixture
def manage_orders_usecase(order_repository_mock, user_repository_mock):
    return ManageOrdersUsecase(order_repository_mock, user_repository_mock)


class TestManageOrdersUsecase:

    def test_get_orders(self, manage_orders_usecase: ManageOrdersUsecase):
        mock_orders = [
            Order(1, OrderStatus.CREATED.value, "Chile", 1),
            Order(2, OrderStatus.CREATED.value, "Chile", 1)
        ]

        manage_orders_usecase.orders_repository.get_orders.return_value = mock_orders

        current_user = {
            "id": 1,
            "role": Roles.MARKETPLACE_USER.value,
        }

        orders = manage_orders_usecase.get_orders(current_user)

        assert len(orders) == len(mock_orders)

    def test_get_order(self, manage_orders_usecase: ManageOrdersUsecase):
        order_id = 1
        mock_order = Order(order_id, OrderStatus.CREATED.value,
                           "Chile", 1)

        current_user = {
            "id": 1,
            "role": Roles.MARKETPLACE_USER.value,
        }

        manage_orders_usecase.orders_repository.get_order.return_value = mock_order
        order = manage_orders_usecase.get_order(order_id, current_user)

        assert order == mock_order

    def test_update_order(self, manage_orders_usecase: ManageOrdersUsecase):
        order_id = 1
        mock_order = Order(order_id, OrderStatus.CREATED.value,
                           "Chile", 1)

        data = mock_order.to_dict()

        manage_orders_usecase.orders_repository.get_order.return_value = mock_order
        manage_orders_usecase.orders_repository.update_order.return_value = mock_order

        current_user = {
            "id": 1,
            "role": Roles.MARKETPLACE_USER.value,
            "status": OrderStatus.CREATED.value
        }

        order = manage_orders_usecase.update_order(
            order_id, data, current_user
        )

        assert order.id == mock_order.id

    def test_delete_order(self, manage_orders_usecase: ManageOrdersUsecase):
        order_id = 1
        mock_order = Order(order_id, OrderStatus.CREATED.value,
                           "Chile", 1)

        manage_orders_usecase.orders_repository.update_order.return_value = mock_order
        manage_orders_usecase.orders_repository.get_order.return_value = mock_order

        current_user = {
            "id": 1,
            "role": Roles.MARKETPLACE_USER.value,
        }

        order = manage_orders_usecase.delete_order(order_id, current_user)

        assert order == mock_order

    def test_add_order(self, manage_orders_usecase: ManageOrdersUsecase):

        data = {
            "status": OrderStatus.CREATED.value,
            "user_id": 1,
            "delivery_address": "Chile"
        }

        mock_order = Order.from_dict(data)

        manage_orders_usecase.orders_repository.add_order.return_value = mock_order

        order = manage_orders_usecase.add_order(user_id=1)

        assert order.user_id == data["user_id"]
        assert order.status == data["status"]
        assert order.delivery_address == data["delivery_address"]

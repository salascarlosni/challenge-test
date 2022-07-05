import pytest

from unittest.mock import Mock

from src.products.entities.product import Product
from src.products.usecases.manage_products_usecase import ManageProductsUsecase


@pytest.fixture
def repository_mock():
    return Mock()


@pytest.fixture
def manage_products_usecase(repository_mock):
    return ManageProductsUsecase(repository_mock)


class TestManageproductsUsecase:

    def test_get_products(self, manage_products_usecase: ManageProductsUsecase):
        mock_products = [
            Product(1, "product 1", "product1 description example", 1, 1),
            Product(2, "product 2", "product2 description example", 2, 1),
        ]

        manage_products_usecase.products_repository.get_products.return_value = mock_products

        products = manage_products_usecase.get_products()

        assert len(products) == len(mock_products)

    def test_get_product(self, manage_products_usecase: ManageProductsUsecase):
        product_id = 1
        mock_product = Product(product_id, "product 1",
                               "product1 description example", 1, 1)

        manage_products_usecase.products_repository.get_product.return_value = mock_product
        products = manage_products_usecase.get_product(product_id)

        assert products == mock_product

    def test_update_product(self, manage_products_usecase: ManageProductsUsecase):
        product_id = 1
        mock_product = Product(id=product_id, name="product 1",
                               short_description="product1 description example", quantity=1, store_id=1)

        data = mock_product.to_dict()

        manage_products_usecase.products_repository.get_product.return_value = mock_product
        manage_products_usecase.products_repository.update_product.return_value = mock_product

        product = manage_products_usecase.update_product(
            product_id, data
        )

        assert product == mock_product

    def test_delete_product(self, manage_products_usecase: ManageProductsUsecase):
        product_id = 1
        mock_product = Product(id=product_id, name="product 1",
                               short_description="product1 description example", quantity=1, store_id=1)

        manage_products_usecase.products_repository.update_product.return_value = mock_product
        manage_products_usecase.products_repository.get_product.return_value = mock_product

        product = manage_products_usecase.delete_product(product_id)

        assert product == mock_product

    def test_create_product(self, manage_products_usecase: ManageProductsUsecase):

        data = {
            "name": "nintendo switch",
            "short_description": "console to play for nintendo",
            "quantity": 1,
            "store_id": 1
        }

        mock_product = Product.from_dict(data)

        manage_products_usecase.products_repository.add_product.return_value = mock_product

        product = manage_products_usecase.add_product(data)

        assert product.name == data["name"]
        assert product.short_description == data["short_description"]
        assert product.quantity == data["quantity"]

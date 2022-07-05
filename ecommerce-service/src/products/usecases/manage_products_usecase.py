from src.utils import utils

from src.products.entities.product import Product
from src.products.repositories.sqlalchemy_product_repository import SQLAlchemyProductRepository


class ManageProductsUsecase:

    def __init__(self, products_repository: SQLAlchemyProductRepository):
        self.products_repository = products_repository

    def get_products(self):
        return self.products_repository.get_products()

    def get_product(self, product_id: int):
        return self.products_repository.get_product(product_id)

    def add_product(self, data):

        current_time = utils.get_current_datetime()
        data["created_at"] = current_time
        data["updated_at"] = current_time
        product = Product.from_dict(data)
        product = self.products_repository.add_product(product)

        return product

    def update_product(self, product_id, data):

        product = self.get_product(product_id)

        if product:

            data["updated_at"] = utils.get_current_datetime()
            product = self.products_repository.update_product(product_id, data)

            return product

        else:
            raise ValueError(f"product of ID {product_id} doesn't exist.")

    def delete_product(self, product_id):

        product = self.get_product(product_id)

        if product:

            data = {
                "deleted_at": utils.get_current_datetime()
            }

            product = self.products_repository.update_product(product_id, data)
            return product

        else:
            raise ValueError(
                f"product of ID {product_id} doesn't exist or is already deleted.")

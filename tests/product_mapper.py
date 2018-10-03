from typing import Dict

from main.adapter.csv_line_mapper import CsvLineMapper, SomeModel
from tests.models.products.product import Product


class ProductLineMapper(CsvLineMapper):
    def to_model(self, line_content: Dict) -> SomeModel:
        id_ = line_content['id']
        name = line_content['name']
        price = line_content['price']

        return Product(id_, name, price)

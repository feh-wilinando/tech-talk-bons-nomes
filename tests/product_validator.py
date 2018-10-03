from typing import Dict, List

from main.adapter.csv_line_validator import CsvLineValidator
from main.infrastructure.message import Message, MessageCategory


class ProductLineValidator(CsvLineValidator):
    def validate(self, line_content: Dict, line_number: int) -> List[Message]:
        error = []

        if line_content['id'] is None:
            error.append(Message(category=MessageCategory.VALIDATION, target='id', key='id_required'))

        if line_content['name'] is None:
            error.append(Message(category=MessageCategory.VALIDATION, target='id', key='name_required'))

        if line_content['price'] is None:
            error.append(Message(category=MessageCategory.VALIDATION, target='id', key='price_required'))
        else:
            try:
                float(line_content['price'])
            except ValueError:
                error.append(Message(category=MessageCategory.VALIDATION, target='id', key='invalid_price_format'))

        return error

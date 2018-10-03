from typing import Dict, List

from main.adapter.csv_line_mapper import CsvLineMapper, SomeModel
from main.adapter.csv_line_validator import CsvLineValidator
from main.infrastructure.message import Message


class CsvLineAdapter(CsvLineMapper, CsvLineValidator):

    def __init__(self, validator: CsvLineValidator, mapper: CsvLineMapper):
        self.validator = validator
        self.mapper = mapper

    def to_model(self, line_content: Dict) -> SomeModel:
        return self.mapper.to_model(line_content)

    def validate(self, line_content: Dict, line_number: int) -> List[Message]:
        return self.validator.validate(line_content, line_number)

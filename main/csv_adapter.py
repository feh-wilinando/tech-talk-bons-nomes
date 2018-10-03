from typing import Dict, List

from main.csv_mapper import CsvMapper, SomeModel
from main.csv_validator import CsvValidator
from main.infrastructure.message import Message


class CsvAdapter(CsvMapper, CsvValidator):

    def __init__(self, validator: CsvValidator, mapper: CsvMapper):
        self.validator = validator
        self.mapper = mapper

    def to_model(self, line_content: Dict) -> SomeModel:
        return self.mapper.to_model(line_content)

    def validate(self, line_content: Dict, line_number: int) -> List[Message]:
        return self.validator.validate(line_content, line_number)

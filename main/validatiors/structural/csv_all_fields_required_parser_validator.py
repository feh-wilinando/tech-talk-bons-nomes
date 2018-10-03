from csv import DictReader
from typing import Dict

from main.infrastructure.either import Left
from main.infrastructure.message import Message, MessageCategory
from main.validatiors.csv_parser_validator_protocol import CsvParserValidatorProtocol


class CsvAllFieldsRequiredParserValidator(CsvParserValidatorProtocol):
    def is_valid(self, reader: DictReader, line: Dict) -> bool:
        values = line.values()

        if not all(values):
            missing_keys = [key for key, value in line.items() if not value]

            message = Message(category=MessageCategory.VALIDATION, key='import_csv_missing_fields',
                              args=[reader.line_num, reader.fieldnames, missing_keys])

            yield Left([message])

            return False

        return True

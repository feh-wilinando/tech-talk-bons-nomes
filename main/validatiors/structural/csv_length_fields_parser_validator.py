from csv import DictReader
from typing import Dict

from main.infrastructure.either import Left
from main.infrastructure.message import Message, MessageCategory
from main.validatiors.csv_parser_validator_protocol import CsvParserValidatorProtocol


class CsvLengthFieldsParserValidator(CsvParserValidatorProtocol):

    def is_valid(self, reader: DictReader, line: Dict) -> bool:
        fields = line.keys()

        if len(fields) > len(reader.fieldnames):
            message = Message(category=MessageCategory.VALIDATION, key='import_csv_enough_fields', args=[reader.line_num, reader.fieldnames])

            yield Left([message])

            return False

        return True


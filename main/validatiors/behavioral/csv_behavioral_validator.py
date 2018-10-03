from csv import DictReader
from typing import Dict

from main.adapter.csv_line_adapter import CsvLineAdapter
from main.infrastructure.either import Left
from main.validatiors.csv_parser_validator_protocol import CsvParserValidatorProtocol


class CsvBehavioralParserValidator(CsvParserValidatorProtocol):

    def __init__(self, adapter: CsvLineAdapter):
        self._adapter = adapter

    def is_valid(self, reader: DictReader, line: Dict) -> bool:
        violations = self._adapter.validate(line, line_number=reader.line_num)

        if violations:
            yield Left(violations)

            return False

        return True

    @staticmethod
    def build(adapter: CsvLineAdapter):
        return CsvBehavioralParserValidator(adapter)

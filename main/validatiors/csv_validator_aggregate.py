from abc import abstractmethod
from csv import DictReader
from typing import Dict, List

from main.adapter.csv_line_adapter import CsvLineAdapter
from main.validatiors.csv_parser_validator_protocol import CsvParserValidatorProtocol


class CsvValidatorAggregate(CsvParserValidatorProtocol):

    def __init__(self, validators: List[CsvParserValidatorProtocol]):
        self._all_validators = validators

    def is_valid(self, reader: DictReader, line: Dict) -> bool:
        for validator in self._all_validators:
            is_valid = yield from validator.is_valid(reader, line)

            if not is_valid:
                return False
        return True

    @staticmethod
    @abstractmethod
    def build(adapter: CsvLineAdapter) -> CsvParserValidatorProtocol:
        ...

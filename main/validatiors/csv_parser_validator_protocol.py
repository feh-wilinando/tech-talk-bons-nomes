from abc import abstractmethod
from csv import DictReader
from typing import Dict


class CsvParserValidatorProtocol:

    @abstractmethod
    def is_valid(self, reader: DictReader, line: Dict) -> bool:
        ...



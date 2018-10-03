from abc import abstractmethod
from typing import Any, Dict, NewType

SomeModel = NewType('SomeModel', object)


class CsvLineMapper:

    @abstractmethod
    def to_model(self, line_content: Dict) -> SomeModel:
        pass

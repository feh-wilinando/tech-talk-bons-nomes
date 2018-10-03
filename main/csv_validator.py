from abc import abstractmethod
from typing import Dict, List

from main.infrastructure.message import Message


class CsvValidator:

    @abstractmethod
    def validate(self, line_content: Dict, line_number: int) -> List[Message]:
        pass

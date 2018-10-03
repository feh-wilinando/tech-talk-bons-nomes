from base64 import b64decode
from csv import DictReader, Sniffer
from io import StringIO
from typing import List, Generator, NewType

from main.adapter.csv_line_adapter import CsvLineAdapter
from main.adapter.csv_line_mapper import SomeModel
from main.infrastructure.either import Left, Right, Either
from main.infrastructure.message import Message, MessageCategory
from main.validatiors.csv_parser_validators import CsvParserValidator

File = NewType('File', object)


class LazyCsvParser:

    def __init__(self, adapter: CsvLineAdapter, fields: List[str]):
        if not fields:
            raise ValueError('Field names required.')

        self._adapter = adapter
        self._fields = fields
        self._parser_validator = CsvParserValidator.build(adapter)

    def read_from_base64(self, content: str, ignore_headers=True) -> Generator[Either[Message, SomeModel], None, None]:
        b64_content = b64decode(content).decode("utf-8")

        some_file = StringIO(b64_content)

        yield from self._read_file_safe(some_file, ignore_headers)

    def read_from_file(self, filename: str, ignore_headers=True) -> Generator[Either[Message, SomeModel], None, None]:
        some_file = open(filename)

        yield from self._read_file_safe(some_file, ignore_headers)

    def _read_file_safe(self, some_file: File, ignore_headers: bool) -> Generator[Either[Message, SomeModel], None, None]:
        sniffer = Sniffer()
        try:
            with some_file as csv:
                dialect = sniffer.sniff(csv.read(1024))

                csv.seek(0)

                reader = DictReader(f=csv, fieldnames=self._fields, dialect=dialect)

                yield from self._read(reader, ignore_headers)
        except Exception as e:
            message = Message(category=MessageCategory.ERROR, key='import_csv_generic_error', args=[e])

            yield Left([message])

    def _read(self, reader: DictReader, ignore_headers: bool) -> Generator[Either[Message, SomeModel], None, None]:
        if ignore_headers:
            next(reader)

        for line_dict in reader:

            is_valid = yield from self._parser_validator.can_parse(reader, line_dict)

            if is_valid:
                try:
                    yield Right(self._adapter.to_model(line_dict))
                except Exception as e:
                    yield Left(e)
            else:
                break

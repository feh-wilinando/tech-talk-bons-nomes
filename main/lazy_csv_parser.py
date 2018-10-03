from io import StringIO
from base64 import b64decode
from csv import DictReader, Sniffer
from typing import List, Generator, NewType, Dict

from main.csv_adapter import CsvAdapter
from main.csv_mapper import SomeModel
from main.infrastructure.either import Left, Right, Either
from main.infrastructure.message import Message, MessageCategory

File = NewType('File', object)


class LazyCsvParser:

    def __init__(self, adapter: CsvAdapter, fields: List[str]):
        if not fields:
            raise ValueError('Field names required.')

        self._adapter = adapter
        self._fields = fields

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

            is_valid = yield from self._validate_structural_and_read_data__Yield_left_messages_to_caller_if_any_validation_fails(reader, line_dict)

            if is_valid:
                try:
                    yield Right(self._adapter.to_model(line_dict))
                except Exception as e:
                    yield Left(e)
            else:
                break

    def _validate_structural_and_read_data__Yield_left_messages_to_caller_if_any_validation_fails(self, reader, line_dict: Dict):

        structure_is_valid = yield from self._validate_structural(reader, line_dict)

        if not structure_is_valid:
            return False

        can_read_data = yield from self._validate_read_data(reader, line_dict)

        return can_read_data

    def _validate_read_data(self, reader: DictReader, line: Dict) -> bool:
        violations = self._adapter.validate(line, line_number=reader.line_num)

        if violations:
            yield Left(violations)

            return False

        return True

    def _validate_structural(self, reader: DictReader, line: Dict) -> bool:
        is_valid_fields_length = yield from self._validate_read_fields_length(reader, line)

        if not is_valid_fields_length:
            return False

        all_fields_required = yield from self._validate_all_fields_required(reader, line)

        if not all_fields_required:
            return False

        return True

    def _validate_read_fields_length(self, reader: DictReader, line: Dict) -> bool:
        fields = line.keys()

        if len(fields) > len(self._fields):
            message = Message(category=MessageCategory.VALIDATION, key='import_csv_enough_fields', args=[reader.line_num, reader.fieldnames])

            yield Left([message])

            return False

        return True

    def _validate_all_fields_required(self, reader: DictReader, line: Dict) -> bool:
        values = line.values()

        if not all(values):
            missing_keys = [key for key, value in line.items() if not value]

            message = Message(category=MessageCategory.VALIDATION, key='import_csv_missing_fields', args=[reader.line_num, reader.fieldnames, missing_keys])

            yield Left([message])

            return False
        return True

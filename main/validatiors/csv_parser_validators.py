from main.adapter.csv_line_adapter import CsvLineAdapter
from main.validatiors.behavioral.csv_behavioral_validator import CsvBehavioralParserValidator
from main.validatiors.csv_parser_validator_protocol import CsvParserValidatorProtocol
from main.validatiors.csv_validator_aggregate import CsvValidatorAggregate
from main.validatiors.structural.csv_structural_parser_validator import CsvStructuralParserValidator


class CsvParserValidator(CsvValidatorAggregate):

    def can_parse(self, reader, line):
        is_valid = yield from self.is_valid(reader, line)

        return is_valid

    @staticmethod
    def build(adapter: CsvLineAdapter) -> CsvParserValidatorProtocol:
        all_validators = [
            CsvStructuralParserValidator.build(adapter),
            CsvBehavioralParserValidator.build(adapter)
        ]

        return CsvParserValidator(all_validators)

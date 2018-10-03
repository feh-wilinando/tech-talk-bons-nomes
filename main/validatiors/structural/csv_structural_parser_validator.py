from main.adapter.csv_line_adapter import CsvLineAdapter
from main.validatiors.csv_validator_aggregate import CsvValidatorAggregate
from main.validatiors.structural.csv_all_fields_required_parser_validator import CsvAllFieldsRequiredParserValidator
from main.validatiors.structural.csv_length_fields_parser_validator import CsvLengthFieldsParserValidator


class CsvStructuralParserValidator(CsvValidatorAggregate):

    @staticmethod
    def build(adapter: CsvLineAdapter):
        all_validators = [
            CsvAllFieldsRequiredParserValidator(),
            CsvLengthFieldsParserValidator()
        ]

        return CsvStructuralParserValidator(all_validators)

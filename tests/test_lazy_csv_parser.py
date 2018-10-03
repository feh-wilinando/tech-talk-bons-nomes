from base64 import b64encode
from random import randint, shuffle

from pytest import fixture, mark

from main.csv_adapter import CsvAdapter
from main.infrastructure.message import MessageCategory
from main.lazy_csv_parser import LazyCsvParser
from tests.models.products.product import Product
from tests.models.products.product_factory import ProductFactory
from tests.product_mapper import ProductMapper
from tests.product_validator import ProductValidator


def generate_csv_for_products_with_header_and_line_format(all_products, header, line_format):
    file_name = 'products.csv'

    with open(file_name, 'w') as csv:
        csv.write(header)

        for product in all_products:
            csv.write(line_format.format(product))

    return file_name


def cast_file_to_base64_string(file_name):
    with open(file_name, 'rb') as csv:
        base64_string = b64encode(csv.read()).decode("utf-8")

    return base64_string


@mark.usefixtures("clean_dir")
class TestLazyCsvParser:

    @fixture
    def number_of_products(self):
        return randint(1, 100)

    @fixture
    def fields(self):
        return list(Product.__dataclass_fields__.keys())

    @fixture
    def all_valid_products(self, number_of_products):
        return ProductFactory.build_batch(number_of_products)

    @fixture
    def all_invalid_products(self, number_of_products):
        return ProductFactory.build_batch(number_of_products, price=0.0)

    @fixture
    def valid_csv_file_name(self, all_valid_products):
        line = '{0.id},{0.name},{0.price}\n'
        header = 'id,name,price\n'

        return generate_csv_for_products_with_header_and_line_format(all_valid_products, header, line)

    @fixture
    def csv_file_with_missing_fields(self, all_valid_products):
        line = '{0.id},{0.name}\n'
        header = 'id,name\n'

        return generate_csv_for_products_with_header_and_line_format(all_valid_products, header, line)

    @fixture
    def csv_file_with_extra_fields(self, all_valid_products):
        line = '{0.id},{0.name},{0.price},xpto\n'
        header = 'id,name,price,xpto\n'

        return generate_csv_for_products_with_header_and_line_format(all_valid_products, header, line)

    @fixture
    def product_adapter(self):
        mapper = ProductMapper()
        validator = ProductValidator()

        return CsvAdapter(validator, mapper)

    @fixture
    def parser(self, product_adapter, fields):
        return LazyCsvParser(product_adapter, fields)

    @fixture
    def csv_file_with_some_validations_errors(self, all_valid_products, all_invalid_products):
        valid_products = ProductFactory.build_batch(4)
        invalid_products = ProductFactory.build_batch(4, price=0.0)

        all_products = valid_products + invalid_products

        shuffle(all_products)

        line = '{0.id},{0.name},{0.price}\n'
        header = 'id,name,price\n'

        return generate_csv_for_products_with_header_and_line_format(all_products, header, line)

    def test_should_read_a_sample_file_with_products(self, valid_csv_file_name, parser):
        generator = parser.read_from_file(valid_csv_file_name)

        assert generator

        for result in generator:
            assert result.is_right

            product = result.value

            assert product.id
            assert product.name
            assert product.price

    def test_should_generate_only_one_error_when_csv_has_missing_fields(self, csv_file_with_missing_fields, parser):
        generator = parser.read_from_file(csv_file_with_missing_fields)

        assert generator

        counter = 0

        for result in generator:
            assert result.is_left

            messages = result.value

            assert 1 == len(messages)

            message = messages[0]

            assert MessageCategory.VALIDATION == message.category

            counter += 1

        assert 1 == counter

    def test_should_generate_only_one_error_when_csv_has_extra_fields(self, csv_file_with_extra_fields, parser):
        generator = parser.read_from_file(csv_file_with_extra_fields)

        assert generator

        counter = 0

        for result in generator:
            assert result.is_left

            messages = result.value

            assert 1 == len(messages)

            message = messages[0]

            assert MessageCategory.VALIDATION == message.category

            counter += 1

        assert 1 == counter

    def test_should_generate_all_validations_errors_per_line_if_exists(self, csv_file_with_some_validations_errors, parser):
        generator = parser.read_from_file(csv_file_with_some_validations_errors)

        assert generator

        counter = 0

        for result in generator:
            assert result

            if result.is_left:
                messages = result.value

                assert 1 == len(messages)

                message = messages[0]

                assert MessageCategory.VALIDATION == message.category
                assert 'price' == messages.targe
            else:
                product = result.value

                assert product.id
                assert product.name
                assert product.price

            counter += 1

        assert 8 == counter

    def test_should_read_a_sample_file_with_products_in_base_64(self, valid_csv_file_name, parser):
        generator = parser.read_from_base64(cast_file_to_base64_string(valid_csv_file_name))

        assert generator

        for result in generator:
            assert result.is_right

            product = result.value

            assert product.id
            assert product.name
            assert product.price

    def test_should_generate_only_one_error_when_csv_has_missing_fields_in_base64(self, csv_file_with_missing_fields, parser):
        generator = parser.read_from_base64(cast_file_to_base64_string(csv_file_with_missing_fields))

        assert generator

        counter = 0

        for result in generator:
            assert result.is_left

            messages = result.value

            assert 1 == len(messages)

            message = messages[0]

            assert MessageCategory.VALIDATION == message.category

            counter += 1

        assert 1 == counter

    def test_should_generate_only_one_error_when_csv_has_extra_fields_in_base64(self, csv_file_with_extra_fields,
                                                                                parser):
        generator = parser.read_from_base64(cast_file_to_base64_string(csv_file_with_extra_fields))

        assert generator

        counter = 0

        for result in generator:
            assert result.is_left

            messages = result.value

            assert 1 == len(messages)

            message = messages[0]

            assert MessageCategory.VALIDATION == message.category

            counter += 1

        assert 1 == counter

    def test_should_generate_all_validations_errors_per_line_if_exists_in_base64(self, csv_file_with_some_validations_errors, parser):
        generator = parser.read_from_base64(cast_file_to_base64_string(csv_file_with_some_validations_errors))

        assert generator

        counter = 0

        for result in generator:
            assert result

            if result.is_left:
                messages = result.value

                assert 1 == len(messages)

                message = messages[0]

                assert MessageCategory.VALIDATION == message.category
                assert 'price' == messages.targe
            else:
                product = result.value

                assert product.id
                assert product.name
                assert product.price

            counter += 1

        assert 8 == counter

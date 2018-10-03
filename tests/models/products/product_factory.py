from functools import partial

from factory import Factory, Faker, Sequence, LazyFunction

from tests.models.products.product import Product


class ProductFactory(Factory):
    class Meta:
        model = Product

    id = Sequence(lambda n: n + 1)
    name = Faker("first_name")
    price = Faker("pyfloat", left_digits=4, right_digits=2, positive=True)

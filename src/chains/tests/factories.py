import factory
from factory.django import DjangoModelFactory

from ..models import Chain


class ChainFactory(DjangoModelFactory):
    class Meta:
        model = Chain

    id = factory.Faker("pystr_format", string_format="#{{random_int}}")
    name = factory.Faker("company")
    rpc_url = factory.Faker("url")
    block_explorer_url = factory.Faker("url")
    currency_name = factory.Faker("cryptocurrency_name")
    currency_symbol = factory.Faker("currency_symbol")
    currency_decimals = factory.Faker("pyint")

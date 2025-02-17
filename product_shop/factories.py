# Generate dummy data
import factory
from faker import Faker
from decimal import Decimal
from django.utils.timezone import now
from product_shop.models import Product, Category

# Initialise the faker
fake = Faker()


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.Iterator(Category.objects.all())
    image = factory.django.ImageField()
    name = factory.LazyAttribute(lambda _: fake.word().capitalize())
    description = factory.LazyAttribute(lambda _: fake.paragraph())
    price = factory.LazyAttribute(
        lambda _: Decimal(fake.random_int(min=1000, max=10000000))
    )
    stock = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=1000))
    avg_rating = factory.LazyAttribute(
        lambda _: Decimal(fake.random.uniform(0, 5)).quantize(Decimal("0.1"))
    )
    created_at = factory.LazyFunction(now)

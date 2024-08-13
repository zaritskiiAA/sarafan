import factory

from sarafan.constants import ImageSizeValues
from users.data_factories.factory import UserFactory
from products.models import (
    ProductCategory, ProductSubCategory, Product,
    CartItem, ShopingCart,
)
from .utils import create_file, create_products_files, get_cart


class CategoryNameSlugAbstractFactory(factory.django.DjangoModelFactory):

    name = factory.Faker("sentence", nb_words=5, locale="ru_RU")
    slug = factory.Faker("sentence", nb_words=5, locale="en_US")

    class Meta:

        abstract = True


class ImageAbstractFactory(factory.django.DjangoModelFactory):

    image = factory.Faker(
        "file_name",
        category='image',
        extension=ImageSizeValues.EXT_IMAGE.value,
    )

    class Meta:

        abstract = True

    @factory.post_generation
    def create_image_file(self, create, extracted, **kwargs):

        create_file(self.image)


class ProductCategoryFactory(
    CategoryNameSlugAbstractFactory, ImageAbstractFactory,
):

    class Meta:

        model = ProductCategory


class ProductSubCategoryFactory(
    CategoryNameSlugAbstractFactory, ImageAbstractFactory,
):

    category = factory.SubFactory(ProductCategoryFactory)

    class Meta:

        model = ProductSubCategory


class ProductFactory(CategoryNameSlugAbstractFactory):

    sub_category = factory.SubFactory(ProductSubCategoryFactory)
    price = factory.Faker('random_number', digits=3)
    big_image = factory.LazyFunction(create_products_files)

    class Meta:

        model = Product


class ShopingCartFactory(factory.django.DjangoModelFactory):

    user = factory.SubFactory(UserFactory)

    class Meta:

        model = ShopingCart


class CartItemFactory(factory.django.DjangoModelFactory):

    cart = factory.LazyFunction(get_cart)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker('random_number', digits=2)

    class Meta:

        model = CartItem

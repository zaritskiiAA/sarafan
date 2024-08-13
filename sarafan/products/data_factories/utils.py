import io
import string
import random

import factory
from PIL import Image
from django.core.files.base import File, ContentFile
from django.contrib.auth import get_user_model

from sarafan.constants import ImageSizeValues
from products.models import CartItem, ShopingCart
from users.data_factories.factory import UserFactory


User = get_user_model()


def generate_bigimage_name(extension: str = '.png') -> str:

    return ''.join(
        string.ascii_letters[random.randint(1, 20)] for _ in range(10)
    ) + extension


def create_file(faker_obj: factory.Faker, sub_dir: str = '') -> str:
    """Создаёт физический файл изображения в media root."""

    stream = io.BytesIO()
    img = Image.new(
        ImageSizeValues.FORMAT_IMAGE.value,
        size=ImageSizeValues.BIG_SIZE.value,
        color=ImageSizeValues.COLOR_IMAGE.value,
    )
    img.save(stream, ImageSizeValues.EXT_IMAGE.value)
    stream.seek(0)
    faker_obj.save(f'{sub_dir}{faker_obj.name}', File(stream))


def create_products_files() -> ContentFile:
    """
    Создаёт физический файл в media root для продукта в 3х экземплярах.
    """
    stream = io.BytesIO()
    img = Image.new(
        ImageSizeValues.FORMAT_IMAGE.value,
        size=ImageSizeValues.BIG_SIZE.value,
        color=ImageSizeValues.COLOR_IMAGE.value,
    )
    img.save(stream, ImageSizeValues.EXT_IMAGE.value)
    return ContentFile(stream.getvalue(), generate_bigimage_name())


def get_cart(user: User | None = None, max_iter=10) -> CartItem:

    if not user:
        users_qs = User.objects.all()
        user = random.choice(users_qs) if users_qs else None
        if not user:
            user = UserFactory.create()
    try:
        qs = ShopingCart.objects.get(user=user)
        print(qs)
    # Костыль.
    except ShopingCart.DoesNotExist:
        if max_iter:
            return get_cart(user=user, max_iter=max_iter-1)
        return qs
    return qs

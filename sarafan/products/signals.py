from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Product
from .utils import ResizeImg


@receiver(post_delete, sender=Product)
def delete_product(
    sender: Product,
    instance: Product,
    using,
    **kwargs,
) -> None:
    """Очищаем изображения из media root если объект продукта удалён."""

    image_name = instance.big_image.name
    ResizeImg.clear(image_name)

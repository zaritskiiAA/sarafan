from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import ShopingCart


User = get_user_model()


@receiver(post_save, sender=User)
def set_shoping_cart_to_new_user(
    sender: User, instance: User, created: bool, **kwargs,
) -> None:

    if created:
        ShopingCart.objects.create(user=instance)

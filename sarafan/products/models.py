from django.contrib.auth import get_user_model
from django.db import models

from sarafan.constants import NumericalValues, ImageSizeValues
from .utils import ResizeImg
from .validators import check_image_name, check_quantity_gross_zero

User = get_user_model()


class ProductCategory(models.Model):

    name = models.CharField(
        max_length=NumericalValues.PRODUCT_CATEGORY_NAME_MAX_LEN,
        verbose_name="Название категории",
    )
    slug = models.SlugField(
        unique=True,
        max_length=NumericalValues.PRODUCT_CATEGORY_SLUG_MAX_LEN,
        verbose_name="Уникальное обозначение категории (слаг).",

    )
    image = models.ImageField(verbose_name="Изображение категории.")

    class Meta:

        verbose_name = 'Категория продуктов.'
        verbose_name_plural = 'Категории продуктов.'
        constraints = [
            models.CheckConstraint(
                name='Имя категории и слаг не могут быть идентичны.',
                check=~models.Q(name=models.F('slug'))
            ),
        ]

    def __str__(self) -> str:
        return self.name


class ProductSubCategory(models.Model):

    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='sub_members',
    )
    name = models.CharField(
        max_length=NumericalValues.PRODUCT_SUBCATEGORY_NAME_MAX_LEN,
        verbose_name="Название подкатегории продукта.",
    )
    slug = models.SlugField(
        unique=True,
        max_length=NumericalValues.PRODUCT_SUBCATEGORY_SLUG_MAX_LEN,
        verbose_name="Уникальное обозначение подкатегории (слаг).",

    )
    image = models.ImageField(verbose_name="Изображение подкатегории.")

    class Meta:

        verbose_name = 'Подкатегория продуктов.'
        verbose_name_plural = 'Подкатегории продуктов.'
        constraints = [
            models.CheckConstraint(
                name='Имя подкатегории и слаг не могут быть идентичны.',
                check=~models.Q(name=models.F('slug'))
            ),
        ]

    def __str__(self) -> str:
        return self.name


class Product(models.Model):

    sub_category = models.ForeignKey(
        ProductSubCategory,
        on_delete=models.CASCADE,
        related_name='products',
    )
    name = models.CharField(
        verbose_name='Название продукта.',
        max_length=NumericalValues.PRODUCT_NAME_MAX_LEN,
    )
    slug = models.SlugField(
        verbose_name="Уникальное обозначение продукта (слаг).",
        unique=True,
        max_length=NumericalValues.PRODUCT_SLUG_MAX_LEN,
    )
    price = models.FloatField(
        verbose_name="Цена продукта.",
    )
    big_image = models.ImageField(
        verbose_name="Изображение продукта 640 x 480.",
        upload_to='products/',
        unique=True,
        validators=(check_image_name,),
    )
    mid_image = models.ImageField(
        verbose_name="Изображение продукта 320 x 240.",
        upload_to='products/',
        blank=True,
    )
    small_image = models.ImageField(
        verbose_name="Изображение продукта 240 x 180.",
        upload_to='products/',
        blank=True,
    )

    class Meta:

        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        constraints = [
            models.CheckConstraint(
                name='Имя продукта и слаг не могут быть идентичны.',
                check=~models.Q(name=models.F('slug'))
            ),
        ]

    def __str__(self) -> str:
        return self.name

    def save(self, **kwargs) -> None:

        target_image = self.big_image

        source_image = Product.objects.filter(pk=self.pk).first()
        # Предположил, что все 3и изображения должны быть
        # одинаковые в разных размерах.
        if any(
            [
                not self.mid_image, not self.small_image,
                (source_image and source_image.big_image != target_image),
            ]
        ):
            self.mid_image = f'products/{self.big_image.name.replace(".", "_mid.")}' # noqa E501
            self.small_image = f'products/{self.big_image.name.replace(".", "_small.")}' # noqa E501
            save_obj = super().save(**kwargs)
            image = ResizeImg(target_image)
            image.resize(ImageSizeValues.BIG_SIZE.value, target_image.path)
            image.resize(ImageSizeValues.MID_SIZE.value, self.mid_image.path),
            image.resize(
                ImageSizeValues.SMALL_SIZE.value, self.small_image.path,
            )
            if (source_image and source_image.big_image != target_image):
                ResizeImg.clear(f'{source_image.big_image.name}')
            return save_obj

        return super().save(**kwargs)


class ShopingCart(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='shoping_cart',
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    def __str__(self) -> str:
        return f'Корзина пользователя {self.user.username}'


class CartItem(models.Model):

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name='cart_items',
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество продукта.', default=1,
        validators=(check_quantity_gross_zero,),
    )
    cart = models.ForeignKey(
        ShopingCart, on_delete=models.CASCADE, related_name='items',
    )

    class Meta:
        verbose_name = 'Объект корзины.'
        verbose_name_plural = 'Объекты корзины.'

    def __str__(self) -> str:
        return self.product.name

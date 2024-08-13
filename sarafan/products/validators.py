from django.core.exceptions import ValidationError


def check_image_name(value: str) -> None | ValidationError:
    """
    Не даём добавлять изображения с некорректными именами,
    например символы которые кодируются, проблема возникает в glob,
    т.к. он не всегда считывает правильно символы с url-кодировкой.
    Допускается только символы "-/_" числа, буквы различных алфавитов.
    """
    try:
        name, _ = value.name.split('.')
    except ValueError:
        raise ValidationError(
            'Изображение может содержать "." только в расширении.'
        )

    if any(
        [
            char for char in name if not char.isdigit() and not char.isalpha() and not char in '-_' # noqa E501
        ]
    ):
        raise ValidationError(
            'Изображение может содержать только буквы, числа и символы "-/_".'
        )


def check_quantity_gross_zero(value: int) -> None | ValidationError:

    if not value:
        raise ValidationError(
            'Количество продукта в коризне не может быть меньше 1.'
        )

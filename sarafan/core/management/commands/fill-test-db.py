from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from products.data_factories.factory import CartItemFactory
from users.data_factories.factory import UserFactory
from products.data_factories.utils import get_cart


class Command(BaseCommand):

    """Класс для наполнения базы данных тестовыми данными."""

    help = "Наполнение базы данных тестовыми данными."

    def add_arguments(self, parser):

        parser.add_argument(
            "-f",
            "--fill",
            action="store_true",
            help="Наполнить базу тестовыми данными.",
        )
        parser.add_argument(
            "-a",
            "--amount",
            type=int,
            default=10,
            help="Количество",
        )
        parser.add_argument(
            "-super",
            "--create_super_user",
            action="store_true",
            help="Создать супер-юзера.",
        )
        parser.add_argument(
            "-c",
            "--my_cart_items",
            action="store_true",
            help="Наполнить корзину конкретного юзера. Дополнительно необходимо указать флаг -id.", # noqa E501
        )
        parser.add_argument(
            "-id",
            "--id_user",
            type=int,
            default=10,
            help="id пользователя для наполнения коризны.",
        )

    def handle(self, *args, **options):
        """Метод для наполнения базы тестовыми данными."""

        fill_db = options.get("fill")
        amount = options.get("amount")
        create_superuser = options.get("create_super_user")
        my_cart_items = options.get("my_cart_items")
        user_id = options.get("id_user")

        if fill_db:
            UserFactory.create_batch(amount)
            CartItemFactory.create_batch(amount)
            return self.stdout.write(
                'База полнена.'
            )
        if create_superuser:

            import os
            from dotenv import load_dotenv
            load_dotenv()

            username = os.getenv('SUPER_USER_NAME')
            email = os.getenv('SUPER_USER_EMAIL')
            password = os.getenv('SUPER_USER_PASSWORD')

            if any([not username, not email, not password]):
                return self.stdout.write(
                    'Проверьте переменные окружения, отсутсвуют данные для создания суперпользователя.' # noqa E501
                )
            get_user_model().objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            return self.stdout.write(
                f'Cуперюзера создан {username}'
            )
        if my_cart_items and user_id:

            CartItemFactory.create_batch(amount, cart=get_cart(user_id))
            return self.stdout.write(
                f'Корзина пользователя {user_id} наполнена.'
            )

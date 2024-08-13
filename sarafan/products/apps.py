from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "products"

    def ready(self) -> None:
        """Импортирование сигналов для приложения."""
        import products.signals  # noqa
        return super().ready()

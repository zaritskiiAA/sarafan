from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self) -> None:
        """Импортирование сигналов для приложения."""
        import users.signals  # noqa
        return super().ready()

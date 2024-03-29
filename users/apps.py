from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "users"

    # Starts signals to create author profile.
    def ready(self):
        from . import signals
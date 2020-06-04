from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'packager.core'

    def ready(self):
        from .models import signals

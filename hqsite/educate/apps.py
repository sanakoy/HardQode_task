from django.apps import AppConfig


class EducateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'educate'

    def ready(self):
        from . import signals

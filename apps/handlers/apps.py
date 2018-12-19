from django.apps import AppConfig

class HandlersConfig(AppConfig):
    name = 'apps.handlers'

    def ready(self):
        from .messages import carrier_start
        carrier_start()
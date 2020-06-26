from django.apps import AppConfig


class EntregarConfig(AppConfig):
    name = 'entregar'

    def ready(self):
        import entregar.signals
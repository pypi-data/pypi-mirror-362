from django.apps import AppConfig


class WhispererConfig(AppConfig):
    name = 'whisperer'

    def ready(self):
        self.module.autodiscover()

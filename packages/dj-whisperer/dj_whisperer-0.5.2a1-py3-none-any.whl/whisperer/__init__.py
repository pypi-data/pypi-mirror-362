from __future__ import unicode_literals

from django.utils.module_loading import autodiscover_modules


def autodiscover():
    from whisperer.events import registry
    from whisperer.tasks import deliver_event

    autodiscover_modules('webhooks', register_to=registry)


default_app_config = 'whisperer.apps.WhispererConfig'

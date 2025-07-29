from django.conf import settings as django_settings

DEFAULT_SETTINGS = {
    "WHISPERER_REQUEST_TIMEOUT": 10,
    "WHISPERER_EVENT_QUEUE_DELAY_SECOND": 360,
    "DEFAULT_AUTO_FIELD": "django.db.models.AutoField",
}


class Settings(object):
    def __getattr__(self, item):
        if item in DEFAULT_SETTINGS:
            return getattr(django_settings, item, DEFAULT_SETTINGS[item])
        raise AttributeError


settings = Settings()

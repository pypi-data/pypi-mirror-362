from __future__ import absolute_import

import os

from celery import Celery

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
app = Celery('tests')

app.config_from_object('django.conf:settings')

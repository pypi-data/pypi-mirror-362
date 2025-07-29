import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from whisperer.countdown import countdown_classes

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField


class StarterModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        update_fields = kwargs.pop('update_fields', None)
        if update_fields is not None:
            if not isinstance(update_fields, list):
                update_fields = list(update_fields)
            update_fields.append('modified_date')
            kwargs['update_fields'] = update_fields
        super(StarterModel, self).save(*args, **kwargs)


class Webhook(StarterModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    target_url = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    secret_key = models.CharField(max_length=124, null=True, blank=True)
    event_type = models.CharField(max_length=124)
    callback = models.CharField(max_length=64, null=True, blank=True)
    retry_countdown_config = JSONField()
    additional_headers = JSONField(default=dict)
    config = JSONField(default=dict)

    def __str__(self):
        return '{}:{}'.format(self.event_type, self.target_url[:25])

    @property
    def countdown(self):
        config = self.retry_countdown_config
        countdown_class = countdown_classes[config['choice']]
        countdown_ = countdown_class(**config['kwargs'])
        return countdown_

    class Meta:
        unique_together = [('user', 'target_url', 'event_type')]


class WebhookEvent(StarterModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    webhook = models.ForeignKey(Webhook, on_delete=models.PROTECT)
    request_payload = JSONField(default=dict)
    response_content = models.TextField()
    response_http_status = models.IntegerField()
    response_time = models.DurationField(null=True, blank=True)
    delivered = models.BooleanField(default=False)
    request_datetimes = ArrayField(
        models.DateTimeField(null=True, blank=True), default=list
    )
    retry_count = models.PositiveIntegerField(null=True)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    object_id = models.CharField(null=True, blank=True, max_length=255)
    content_object = GenericForeignKey()

    def __str__(self):
        return '{}:{}'.format(self.webhook, self.delivered)

    @property
    def is_retry_allowed(self):
        countdown = self.webhook.countdown
        return (
            self.created_date + timedelta(seconds=countdown.get_value(self.retry_count))
        ) <= timezone.now()


class EventQueue(StarterModel):

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)

    hook_id = models.PositiveIntegerField()

    event_type = models.CharField(max_length=124)

    app_label = models.CharField(null=True, blank=True, max_length=124)

    model_name = models.CharField(null=True, blank=True, max_length=124)

    object_id = models.CharField(null=True, blank=True, max_length=255)

    instance_dict = JSONField(default=dict)

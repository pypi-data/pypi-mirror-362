import json
import logging
from datetime import timedelta

import requests
from celery import current_app
from django.apps import apps
from django.db import models
from django.db.models import F
from django.db.models.functions import Coalesce

try:
    from django.db.models.functions.datetime import Now
except ImportError:
    from django.db.models.functions import Now
from django.db.transaction import atomic
from django.utils import timezone
from django.utils.module_loading import import_string
from rest_framework.utils.encoders import JSONEncoder

from whisperer.client import WebhookClient
from whisperer.conf import settings
from whisperer.events import registry
from whisperer.exceptions import (
    EventAlreadyDelivered,
    UnknownEventType,
    WebhookEventDoesNotExist,
)
from whisperer.services import EventQueueService
from whisperer.utils import LockTask, Slices

TASK_RETRY_COUNT = 10
MAX_RETRY_COUNT = 18
logger = logging.getLogger(__name__)


def get_natural_key(instance):
    from django.contrib.contenttypes.models import ContentType

    content_type = ContentType.objects.get_for_model(instance)
    return content_type.natural_key()


@current_app.task(
    bind=True, acks_late=True, max_retries=TASK_RETRY_COUNT, base=LockTask
)
def deliver_event_task(
    self,
    hook_id,
    event_type,
    event_queue_uuid=None,
    event_uuid=None,
    instance=None,
    app_label=None,
    model_name=None,
    pk=None,
    retry=True,
    **kwargs
):
    if not event_uuid and not (pk or instance):
        logger.error("Both pk and instance can not be null")
        return

    from whisperer.models import EventQueue, Webhook

    if event_queue_uuid:
        exists = EventQueue.objects.filter(uuid=event_queue_uuid).exists()
        if not exists:
            # This means task is duplicate and already executed
            return

    hook = Webhook.objects.get(pk=hook_id)
    if not event_uuid and not instance and app_label and model_name and pk:
        object_deleted = False
        if event_type not in registry:
            logger.error(
                "Event type '{event_type}' is not registered".format(
                    event_type=event_type
                )
            )
            return
        event_class = registry[event_type]
        if event_class.queryset:
            try:
                instance = event_class.queryset.get(pk=pk)
            except event_class.queryset.model.DoesNotExist:
                object_deleted = True
        else:
            model_class = apps.get_model(app_label, model_name)
            try:
                instance = model_class.objects.get(pk=pk)
            except model_class.DoesNotExist:
                object_deleted = True
        if object_deleted:
            # Object deleted before the task started
            if event_queue_uuid:
                # clear event_queue object so event can't be triggered
                # indefinitely
                EventQueue.objects.filter(uuid=event_queue_uuid).delete()

            return

    webhook_event, response = _deliver_event(
        hook,
        instance,
        event_type,
        event_uuid=event_uuid,
        event_queue_uuid=event_queue_uuid,
    )
    # Set back the original event_queue_uuid None before retrying
    self.request.kwargs['event_queue_uuid'] = None

    if not response.ok:
        self.request.kwargs['event_uuid'] = webhook_event.uuid
        webhook_event.refresh_from_db(fields=['retry_count'])
        webhook_event_retry_count = webhook_event.retry_count or 1
        if (
            self.request.retries >= TASK_RETRY_COUNT
            or webhook_event_retry_count >= MAX_RETRY_COUNT
            or not retry
        ):
            return webhook_event.pk

        self.retry(countdown=hook.countdown.get_value(self.request.retries))

    return webhook_event.pk


@atomic()
def _deliver_event(
    hook, instance, event_type, event_uuid=None, event_queue_uuid=None, force=False
):
    from django.contrib.contenttypes.models import ContentType

    from whisperer.models import EventQueue, WebhookEvent

    if event_type not in registry:
        raise UnknownEventType()

    if event_uuid:
        try:
            # Prevent multiple modification so request for single event triggers one at a time
            webhook_event = WebhookEvent.objects.select_for_update().get(
                uuid=event_uuid
            )
            payload = webhook_event.request_payload
            if webhook_event.delivered and not force:
                raise EventAlreadyDelivered()
        except WebhookEvent.DoesNotExist:
            raise WebhookEventDoesNotExist()
    else:
        webhook_event = WebhookEvent(webhook=hook, retry_count=0)
        event_class = registry[event_type]
        event = event_class()
        serialize_instance = event.serialize(instance)
        payload = {
            'event': {'type': event_type, 'uuid': webhook_event.uuid.hex},
            'payload': serialize_instance,
        }
        payload = event.customize_payload(payload)

    request_datetime = timezone.now()
    response = requests.Response()
    try:
        client = WebhookClient(event_type=event_type, payload=payload)
        response = client.send_payload(
            target_url=hook.target_url,
            payload=payload,
            secret_key=hook.secret_key,
            additional_headers=hook.additional_headers,
            auth_config=hook.config.get('auth'),
        )
    except requests.exceptions.RequestException as exc:
        response.status_code = (exc.response and exc.response.status_code) or 500
        response._content = exc
    except Exception as exc:
        response._content = ''
        response.status_code = 500
        logger.exception(exc)
    finally:
        webhook_event.request_payload = json.loads(json.dumps(payload, cls=JSONEncoder))
        webhook_event.response_content = response.content
        webhook_event.response_http_status = response.status_code
        webhook_event.response_time = timezone.now() - request_datetime
        if isinstance(instance, (models.Model, models.base.ModelBase)):
            webhook_event.object_id = instance.pk
            webhook_event.content_object = instance
            webhook_event.content_type = ContentType.objects.get_for_model(
                instance._meta.model
            )
        if 200 <= response.status_code < 300:
            webhook_event.delivered = True
        else:
            webhook_event.delivered = False
        webhook_event.request_datetimes.insert(0, request_datetime)
        webhook_event.retry_count = (
            Coalesce(F('retry_count') + 1, len(webhook_event.request_datetimes))
            if webhook_event.pk
            else 1
        )
        webhook_event.save()
        if event_queue_uuid:
            EventQueue.objects.filter(uuid=event_queue_uuid).delete()

    if hook.callback:
        callback_function = import_string(hook.callback)
        callback_function(response, event_type, instance, payload)

    return webhook_event, response


def deliver_event(
    instance, event_type, async_=True, event_uuid=None, config_filter=None
):
    from whisperer.models import Webhook

    queue_service = EventQueueService()
    hooks = Webhook.objects.filter(event_type=event_type, is_active=True)

    if config_filter:
        hooks = hooks.filter(
            **{'config__{}'.format(k): v for k, v in config_filter.items()}
        )

    for hook in hooks:
        if not async_:
            _deliver_event(hook, instance, event_type, event_uuid)
            continue
        if isinstance(instance, (models.Model, models.base.ModelBase)):
            app_label, model_name = get_natural_key(instance)
            logger.warning(
                "Delivering event '{0}' for model: {1}.{2} with instance pk {3}. hook pk: {4}".format(
                    event_type, app_label, model_name, instance.pk, hook.pk
                )
            )
            event_queue_instance = queue_service.create_event_queue(
                hook_id=hook.pk,
                event_type=event_type,
                app_label=app_label,
                model_name=model_name,
                object_id=str(instance.pk),
            )
            deliver_event_task.delay(
                hook_id=hook.pk,
                event_type=event_type,
                event_queue_uuid=event_queue_instance.uuid,
                app_label=app_label,
                model_name=model_name,
                pk=str(instance.pk),
                event_uuid=event_uuid,
            )
        elif isinstance(instance, dict):
            event_queue_instance = queue_service.create_event_queue(
                hook_id=hook.pk, event_type=event_type, instance_dict=instance
            )
            deliver_event_task.delay(
                hook_id=hook.pk,
                event_type=event_type,
                event_queue_uuid=event_queue_instance.uuid,
                instance=instance,
                event_uuid=event_uuid,
            )
        else:
            raise NotImplementedError()


@current_app.task()
def undelivered_event_scanner():
    from whisperer.models import WebhookEvent

    undelivered_events = WebhookEvent.objects.filter(
        retry_count__gte=TASK_RETRY_COUNT + 1,
        retry_count__lte=MAX_RETRY_COUNT,
        delivered=False,
    ).all()

    for undelivered_event in undelivered_events:
        if undelivered_event.is_retry_allowed:
            deliver_event_task.delay(
                hook_id=undelivered_event.webhook_id,
                event_type=undelivered_event.webhook.event_type,
                event_uuid=undelivered_event.uuid,
                retry=False,
            )


@current_app.task()
def trigger_deliver_events_with_event_queue(event_queue_ids):
    from whisperer.models import EventQueue

    event_queues = EventQueue.objects.filter(pk__in=event_queue_ids).all()

    for event_queue in event_queues:
        if event_queue.object_id:
            deliver_event_task.delay(
                hook_id=event_queue.hook_id,
                event_type=event_queue.event_type,
                event_queue_uuid=event_queue.uuid,
                app_label=event_queue.app_label,
                model_name=event_queue.model_name,
                pk=event_queue.object_id,
                event_uuid=None,
            )
        else:
            deliver_event_task.delay(
                hook_id=event_queue.hook_id,
                event_type=event_queue.event_type,
                event_queue_uuid=event_queue.uuid,
                instance=event_queue.instance_dict,
                event_uuid=None,
            )


@current_app.task()
def trigger_event_queue_events():
    """
    Process events within a specific time interval.
    batch_minutes: Duration in minutes for each batch to process
    limit: Maximum number of events to process in a batch
    """
    from whisperer.models import EventQueue

    now = timezone.now()

    delayed_time_seconds = settings.WHISPERER_EVENT_QUEUE_DELAY_SECOND
    delayed_time = now - timezone.timedelta(seconds=delayed_time_seconds)
    this_week = now - timezone.timedelta(weeks=1)

    event_queue_ids_list = list(
        EventQueue.objects.filter(
            created_date__gte=this_week, modified_date__lt=delayed_time
        ).values_list('pk', flat=True)
    )

    for chunked_ids_list in Slices(event_queue_ids_list, 1000):
        trigger_deliver_events_with_event_queue.delay(event_queue_ids=chunked_ids_list)
        # Updating triggered EventQueues so it can wait
        # another WHISPERER_EVENT_QUEUE_DELAY_SECOND to re-trigger if it lost again.
        EventQueue.objects.filter(pk__in=chunked_ids_list).update(modified_date=Now())


@current_app.task(base=LockTask)
def delete_outdated_webhook_events(older_than_weeks=12, limit=10000):
    from whisperer.models import WebhookEvent

    threshold_date = timezone.now() - timedelta(weeks=older_than_weeks)

    outdated_webhook_items = WebhookEvent.objects.filter(
        modified_date__lte=threshold_date
    )[:limit]

    try:
        WebhookEvent.objects.filter(id__in=outdated_webhook_items).delete()
    except Exception as exc:
        logger.error(str(exc))

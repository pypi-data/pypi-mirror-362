import logging

from whisperer.exceptions import (
    EventAlreadyDelivered,
    EventStillInProgress,
    WebhookAlreadyRegistered,
)
from whisperer.models import EventQueue, Webhook, WebhookEvent

logger = logging.getLogger(__name__)


class WebhookService(object):
    def register_webhook(self, user, *args, **kwargs):
        event_type = kwargs.get('event_type')
        target_url = kwargs.get('target_url')
        try:
            Webhook.objects.get(user=user, target_url=target_url, event_type=event_type)
            raise WebhookAlreadyRegistered()
        except Webhook.DoesNotExist:
            pass
        webhook = Webhook(user=user)
        for attr, value in kwargs.items():
            setattr(webhook, attr, value)
        webhook.save()
        return webhook

    def update_webhook(self, webhook, user, *args, **kwargs):
        webhook.user = user
        target_url = kwargs.get('target_url', webhook.target_url)
        event_type = kwargs.get('event_type', webhook.event_type)
        try:
            Webhook.objects.exclude(id=webhook.id).get(
                user=user, target_url=target_url, event_type=event_type
            )
            raise WebhookAlreadyRegistered()
        except Webhook.DoesNotExist:
            pass

        for attr, value in kwargs.items():
            setattr(webhook, attr, value)
        webhook.save(update_fields=kwargs.keys())
        return webhook

    def delete_webhook(self, webhook):
        webhook.is_active = False
        webhook.save(update_fields=['is_active'])


class WebhookEventService:
    @staticmethod
    def retry_webhook_event(webhook_event, force=False):
        # type: (WebhookEvent, bool) -> dict

        from whisperer.tasks import _deliver_event

        if webhook_event.delivered:
            raise EventAlreadyDelivered()

        if not force and webhook_event.retry_count < 11:
            raise EventStillInProgress()

        event, response = _deliver_event(
            webhook_event.webhook,
            instance=None,
            event_type=webhook_event.webhook.event_type,
            event_uuid=webhook_event.uuid,
        )
        detail_text = (
            "Webhook event delivered successfully"
            if response.ok
            else "Webhook event delivery failed"
        )
        return {
            "detail": detail_text,
            "response_status": response.status_code,
            "response_content": response.text,
            "delivered": response.ok,
            "response_time": event.response_time,
        }


class EventQueueService(object):
    @staticmethod
    def create_event_queue(
        hook_id,
        event_type,
        app_label=None,
        model_name=None,
        object_id=None,
        instance_dict=None,
    ):
        if instance_dict is None:
            instance_dict = {}
        instance = EventQueue(
            hook_id=hook_id,
            event_type=event_type,
            app_label=app_label,
            model_name=model_name,
            object_id=object_id,
            instance_dict=instance_dict,
        )
        instance.save()

        logger.warning(
            "EventQueue created: {0} for hook {1} with event type {2}".format(
                instance.id, hook_id, event_type
            )
        )

        return instance

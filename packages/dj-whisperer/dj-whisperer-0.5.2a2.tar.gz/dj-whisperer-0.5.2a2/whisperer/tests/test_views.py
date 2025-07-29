import sys
from collections import namedtuple
from datetime import timedelta

import requests_mock
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from mock import patch
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from whisperer.models import EventQueue, Webhook, WebhookEvent
from whisperer.resources.views import (
    EventQueueViewSet,
    WebhookEventViewSet,
    WebhookViewSet,
)


@override_settings(ROOT_URLCONF='whisperer.urls')
class WebhookViewSetTestCase(APITestCase):
    BASE_URL = "/hooks/"

    def setUp(self):
        self.user = mommy.make(User, username="test_admin_user", is_superuser=True)
        self.dummy_user = mommy.make(User, username="dummy_user", is_superuser=False)
        dummy_user_b = mommy.make(User, username="dummy_userb", is_superuser=False)
        self.client.force_authenticate(user=self.user)
        mommy.make(
            Webhook,
            user=self.dummy_user,
            retry_countdown_config={"choice": "exponential", "kwargs": {"base": 2}},
            additional_headers={},
            config={},
            _quantity=5,
        )
        mommy.make(
            Webhook,
            user=dummy_user_b,
            retry_countdown_config={"choice": "exponential", "kwargs": {"base": 2}},
            additional_headers={},
            config={},
            _quantity=5,
        )

    def test_list_with_admin_user(self):
        request = namedtuple("Request", ["user"])
        view = WebhookViewSet(request=request(user=self.user))
        qs = view.get_queryset()
        self.assertEqual(qs.count(), 10)

    def test_list_with_regular_user(self):
        request = namedtuple("Request", ["user"])
        view = WebhookViewSet(request=request(user=self.dummy_user))
        qs = view.get_queryset()
        self.assertEqual(qs.count(), 5)

    def test_get_registry(self):
        response = self.client.get(reverse("webhook-get-registry"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_target_url_filter(self):
        webhook = Webhook.objects.last()
        target_url = webhook.target_url
        url = "{}?target_url={}".format(self.BASE_URL, target_url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], webhook.id)

    def test_is_active_filter(self):
        mommy.make(
            Webhook,
            user=self.user,
            retry_countdown_config={"choice": "exponential", "kwargs": {"base": 2}},
            additional_headers={},
            config={},
            is_active=False,
            _quantity=3,
        )
        url = "{}?is_active=False".format(self.BASE_URL)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        query = Webhook.objects.filter(is_active=False)
        response_ids = [item["id"] for item in response.json()]
        expected_ids = query.values_list("id", flat=True)

        self.assertEqual(len(response.json()), query.count())
        self.assertEqual(sorted(response_ids), sorted(expected_ids))

    def test_event_type_filter(self):
        webhook = Webhook.objects.last()
        webhook.event_type = "order-created"
        webhook.save()

        url = "{}?event_type=order-created".format(self.BASE_URL)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], webhook.id)


@override_settings(ROOT_URLCONF='whisperer.urls')
class WebhookEventViewSetTestCase(APITestCase):
    BASE_URL = "/hook_events/"

    def setUp(self):
        self.date_format = "%Y-%m-%d"
        self.target_url = "http://example.com/order_create"
        self.user = mommy.make(User, username="test_admin_user", is_superuser=True)
        self.dummy_user = mommy.make(User, username="dummy_user", is_superuser=False)
        dummy_user_b = mommy.make(User, username="dummy_userb", is_superuser=False)
        self.client.force_authenticate(user=self.user)

        self.webhook_a = mommy.make(
            Webhook,
            user=self.dummy_user,
            retry_countdown_config={"choice": "exponential", "kwargs": {"base": 2}},
            additional_headers={},
            config={},
        )
        self.webhook_b = mommy.make(
            Webhook,
            user=dummy_user_b,
            target_url=self.target_url,
            retry_countdown_config={"choice": "exponential", "kwargs": {"base": 2}},
            additional_headers={},
            config={},
            event_type="order-created",
        )
        self.now = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.one_day_early = self.now - timedelta(days=1)
        self.event_1 = mommy.make(
            WebhookEvent,
            webhook=self.webhook_a,
            request_payload={},
            content_type_id=1,
            object_id="1",
        )
        self.event_2 = mommy.make(
            WebhookEvent,
            webhook=self.webhook_a,
            request_payload={},
            content_type_id=2,
            object_id="2",
        )
        mommy.make(
            WebhookEvent, webhook=self.webhook_a, request_payload={}, _quantity=5
        )
        mommy.make(
            WebhookEvent, webhook=self.webhook_b, request_payload={}, _quantity=5
        )
        self.event = WebhookEvent.objects.last()
        self.event.created_date = self.one_day_early
        self.event.save()

    def test_list_with_admin_user(self):
        request = namedtuple("Request", ["user"])
        view = WebhookEventViewSet(request=request(user=self.user))
        qs = view.get_queryset()
        self.assertEqual(qs.count(), 12)

    def test_list_with_regular_user(self):
        request = namedtuple("Request", ["user"])
        view = WebhookEventViewSet(request=request(user=self.dummy_user))
        qs = view.get_queryset()
        self.assertEqual(qs.count(), 7)

    def test_event_type_filter(self):
        webhook_event = WebhookEvent.objects.last()
        webhook_event.webhook.event_type = "order-created"
        webhook_event.webhook.save()

        url = "{}?event_type=order-created".format(self.BASE_URL)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        query = WebhookEvent.objects.filter(webhook__event_type="order-created")
        response_ids = [item["id"] for item in response.json()]
        expected_ids = query.values_list("id", flat=True)
        self.assertEqual(len(response.json()), query.count())
        self.assertEqual(sorted(response_ids), sorted(expected_ids))

    def test_delivered_filter(self):
        webhook_event = WebhookEvent.objects.last()
        webhook_event.delivered = True
        webhook_event.save()

        url = "{}?delivered=True".format(self.BASE_URL)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        query = WebhookEvent.objects.filter(delivered=True)
        reponse_ids = [item["id"] for item in response.json()]
        expected_ids = query.values_list("id", flat=True)

        self.assertEqual(len(response.json()), query.count())
        self.assertEqual(sorted(reponse_ids), sorted(expected_ids))

    def test_uuid_filter(self):
        webhook_event = WebhookEvent.objects.last()
        url = "{}?uuid={}".format(self.BASE_URL, webhook_event.uuid)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], webhook_event.id)

    def test_response_http_status_filter(self):
        webhook_event = WebhookEvent.objects.last()
        webhook_event.response_http_status = 500
        webhook_event.save()
        url = "{}?response_http_status=500".format(self.BASE_URL)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        query = WebhookEvent.objects.filter(response_http_status=500)
        response_ids = [item["id"] for item in response.json()]
        expected_ids = query.values_list("id", flat=True)

        self.assertEqual(len(response.json()), query.count())
        self.assertEqual(sorted(response_ids), sorted(expected_ids))

    def test_created_date_filter(self):
        url = "{}?created_date={}".format(
            self.BASE_URL, self.one_day_early.strftime(self.date_format)
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], self.event.id)

    def test_created_date__gt_filter(self):
        url = "{}?created_date__gt={}".format(
            self.BASE_URL, self.now.strftime(self.date_format)
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 11)

    def test_created_date__gte_filter(self):
        url = "{}?created_date__gte={}".format(
            self.BASE_URL, self.one_day_early.strftime(self.date_format)
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 12)

    def test_created_date__lt_filter(self):
        url = "{}?created_date__lt={}".format(
            self.BASE_URL, self.now.strftime(self.date_format)
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], self.event.id)

    def test_created_date__lte_filter(self):
        date = self.one_day_early
        url = "{}?created_date__lte={}".format(
            self.BASE_URL, date.strftime(self.date_format)
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], self.event.id)

    def test_content_type_filter(self):
        url = "{}?content_type={}".format(self.BASE_URL, 1)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], self.event_1.id)

    def test_object_id_filter(self):
        url = "{}?object_id={}".format(self.BASE_URL, 2)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], self.event_2.id)

    def test_webhook_id_filter(self):
        url = "{}?webhook={}".format(self.BASE_URL, self.webhook_b.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 5)

        for item in response.json():
            self.assertEqual(item["webhook"]["id"], self.webhook_b.id)

    def test_retry_webhook_event_sync_success(self):
        self.event.delivered = False
        self.event.retry_count = 11
        self.event.save()

        url = "{}{}/retry/".format(self.BASE_URL, self.event.id)

        with requests_mock.Mocker() as mock:
            mock.register_uri(
                "POST", self.event.webhook.target_url, text="Foo", status_code=200
            )
            response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()["delivered"])
        self.assertEqual(response.json()["response_status"], 200)
        self.assertEqual(response.json()["response_content"], "Foo")
        self.assertEqual(
            response.json()["detail"], "Webhook event delivered successfully"
        )

        self.event.refresh_from_db()
        self.assertEqual(self.event.delivered, True)
        self.assertEqual(self.event.retry_count, 12)
        self.assertEqual(self.event.response_http_status, 200)
        self.assertGreater(self.event.response_time.total_seconds(), 0)
        self.assertIn("Foo", self.event.response_content)

    def test_retry_webhook_event_sync_failure(self):
        self.event.delivered = False
        self.event.retry_count = 11
        self.event.save()

        url = "{}{}/retry/".format(self.BASE_URL, self.event.id)

        with requests_mock.Mocker() as mock:
            mock.register_uri(
                "POST", self.event.webhook.target_url, text="Foo", status_code=400
            )
            response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertFalse(response.json()["delivered"])
        self.assertEqual(response.json()["response_status"], 400)
        self.assertEqual(response.json()["response_content"], "Foo")
        self.assertEqual(response.json()["detail"], "Webhook event delivery failed")

        self.event.refresh_from_db()
        self.assertEqual(self.event.delivered, False)
        self.assertEqual(self.event.retry_count, 12)
        self.assertEqual(self.event.response_http_status, 400)
        self.assertGreater(self.event.response_time.total_seconds(), 0)
        self.assertIn("Foo", self.event.response_content)

    def test_retry_already_delivered_webhook_event(self):
        self.event.delivered = True
        self.event.retry_count = 11
        self.event.save()

        url = "{}{}/retry/".format(self.BASE_URL, self.event.id)

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.json()["code"], "event_100_3")
        self.assertEqual(response.json()["en"], "Event already delivered")

    def test_retry_webhook_event_in_retry_process(self):
        self.event.delivered = False
        self.event.retry_count = 5
        self.event.save()

        url = "{}{}/retry/".format(self.BASE_URL, self.event.id)

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.json()["code"], "event_100_6")
        self.assertEqual(response.json()["en"], "Event is still in retry process")

    def test_retry_webhook_event_with_force_delivered(self):
        self.event.delivered = False
        self.event.retry_count = 5
        self.event.save()

        url = "{}{}/retry/".format(self.BASE_URL, self.event.id)

        with requests_mock.Mocker() as mock:
            mock.register_uri(
                "POST", self.event.webhook.target_url, text="Foo", status_code=200
            )
            response = self.client.post(url, {"force": True})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()["delivered"])
        self.assertEqual(response.json()["response_status"], 200)
        self.assertEqual(response.json()["response_content"], "Foo")
        self.assertEqual(
            response.json()["detail"], "Webhook event delivered successfully"
        )

        self.event.refresh_from_db()
        self.assertEqual(self.event.delivered, True)
        self.assertEqual(self.event.retry_count, 6)
        self.assertEqual(self.event.response_http_status, 200)
        self.assertGreater(self.event.response_time.total_seconds(), 0)
        self.assertIn("Foo", self.event.response_content)


@override_settings(ROOT_URLCONF="whisperer.urls")
class EventQueueViewSetTestCase(TestCase):
    BASE_URL = "/event_queues/"

    def setUp(self):
        self.user = mommy.make(User, username="test_admin_user", is_superuser=True)
        mommy.make(EventQueue, event_type="order-created")
        mommy.make(EventQueue, event_type="product-updated")

    def test_list_with_admin_user(self):
        request = namedtuple("Request", ["user"])
        view = EventQueueViewSet(request=request(user=self.user))
        qs = view.get_queryset()
        self.assertEqual(qs.count(), 2)

    def test_event_type_filter(self):
        event_queue = mommy.make(EventQueue, event_type="product-created")
        url = "{}?event_type={}".format(self.BASE_URL, "product-created")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], event_queue.id)

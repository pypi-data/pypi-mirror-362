from django.test import TestCase
from rest_framework.exceptions import ValidationError

from whisperer.resources.serializers import WebhookSerializer


class WebhookSerializerTestCase(TestCase):
    serializer = WebhookSerializer
    data = {
        "retry_countdown_config": {"choice": "fixed", "kwargs": {"seconds": 60}},
        "target_url": "https://example.com",
    }

    def test_valid_data(self):
        self.data["event_type"] = "order-created"
        serializer = self.serializer(data=self.data)
        serializer.is_valid(raise_exception=True)

    def test_invalid_event_type(self):
        self.data["event_type"] = "invalid.event"
        serializer = self.serializer(data=self.data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

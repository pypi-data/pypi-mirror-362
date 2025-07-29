from django.db.models.signals import post_save, pre_delete

from whisperer.events import WhispererEvent, registry
from whisperer.tasks import deliver_event
from whisperer.tests.models import Foo, Order
from whisperer.tests.serializers import FooSerializer, OrderSerializer


class OrderCreateEvent(WhispererEvent):
    serializer_class = OrderSerializer
    event_type = 'order-created'
    queryset = Order.objects.select_related(
        "customer",
        "address",
    ).all()


class OrderUpdateEvent(WhispererEvent):
    serializer_class = OrderSerializer
    event_type = 'order-updated'


class OrderDeleteEvent(WhispererEvent):
    serializer_class = OrderSerializer
    event_type = 'order-deleted'


class FooCreateEvent(WhispererEvent):
    serializer_class = FooSerializer
    event_type = 'foo-created'


class FooUpdateEvent(WhispererEvent):
    serializer_class = FooSerializer
    event_type = 'foo-updated'


class FooDeleteEvent(WhispererEvent):
    event_type = 'foo-deleted'


class FooChannelEvent(WhispererEvent):
    serializer_class = OrderSerializer
    event_type = 'foo-channel'


registry.register(OrderCreateEvent)
registry.register(OrderUpdateEvent)
registry.register(OrderDeleteEvent)
registry.register(FooCreateEvent)
registry.register(FooUpdateEvent)
registry.register(FooDeleteEvent)
registry.register(FooChannelEvent)


def signal_receiver(instance, created=False, **kwargs):
    if created:
        deliver_event(instance, 'order-created')
    else:
        deliver_event(instance, 'order-updated')


def signal_delete_receiver(sender, instance, created=False, **kwargs):
    order_data = OrderSerializer(instance).data

    deliver_event(order_data, 'order-deleted')


def signal_foo_receiver(instance, created=False, **kwargs):
    if created:
        deliver_event(instance, 'foo-created')
    else:
        deliver_event(instance, 'foo-updated')


def signal_foo_delete_receiver(sender, instance, created=False, **kwargs):
    foo_data = FooSerializer(instance).data

    deliver_event(foo_data, 'foo-deleted')


post_save.connect(signal_receiver, Order)
pre_delete.connect(signal_delete_receiver, sender=Order)
post_save.connect(signal_foo_receiver, Foo)
pre_delete.connect(signal_foo_delete_receiver, sender=Foo)

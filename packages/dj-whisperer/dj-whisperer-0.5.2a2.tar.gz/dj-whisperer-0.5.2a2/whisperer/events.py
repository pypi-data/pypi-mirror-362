from django.core import serializers

from whisperer.exceptions import AlreadyRegisteredEvent, ImproperlyConfigured


class WhispererEvent(object):
    serializer_class = None
    event_type = None
    queryset = None

    def _serialize(self, instance):
        objects = [instance] if not isinstance(instance, list) else instance
        return serializers.serialize('json', objects)

    def serialize(self, instance):
        if isinstance(instance, dict):
            return instance

        if self.serializer_class is None:
            return self._serialize(instance)

        many = isinstance(instance, list)
        return self.serializer_class(instance, many=many).data

    def customize_payload(self, payload):
        return payload


class EventRegistry(object):
    def __init__(self):
        self._registry = {}

    def __contains__(self, event_type):
        return event_type in self._registry

    def __getitem__(self, event_type):
        return self._registry[event_type]

    def keys(self):
        return self._registry.keys()

    @property
    def event_types(self):
        return self._registry.keys()

    @property
    def event_type_choices(self):
        event_types = self.event_types
        return zip(event_types, event_types)

    def register(self, *events):
        for event in events:
            if not issubclass(event, WhispererEvent):
                raise ImproperlyConfigured()

            if event.event_type in self._registry:
                raise AlreadyRegisteredEvent(params=(event.event_type,))

            self._registry[event.event_type] = event


registry = EventRegistry()

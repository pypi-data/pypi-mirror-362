Django Whisperer
===================

Stay informed of it! Django Whisperer informs subscribed users via an URL when a specific event occurs. Currently only works on PostgreSQL.

Let's have a look:

.. code-block:: python

    from whisperer.events import WhispererEvent, registry
    from whisperer.tasks import deliver_event
    from django.db.models.signals import post_save

    class PackageCreateEvent(WhispererEvent):
        serializer_class = PackageSerializer
        event_type = 'package-created'

    registry.register(PackageCreateEvent)


    def signal_receiver(instance, created=False, **kwargs):
        if created:
            deliver_event(instance, 'package-created')

    post_save.connect(signal_receiver, Package)


This will informs subscribed users when a package created with the following payload:

.. code-block:: python

    >>> webhook_event.request_payload
    '{"event": {"type": "package-created", "uuid": "da81e85139824c6187dd1e58a7d3f971"}, "data": {"...": "..."}}'

``data`` contains serialized data of the instance which triggered the whisperer event.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   quickstart
   advanced

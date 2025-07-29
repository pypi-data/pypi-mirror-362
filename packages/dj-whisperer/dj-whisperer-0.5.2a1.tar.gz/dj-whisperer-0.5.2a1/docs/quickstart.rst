Quick Start
===========

This page shows some examples of the basic usage.

Creating a Whisperer Event
--------------------------

Let's define a Whisperer Event.

.. code-block:: python

    from whisperer.events import WhispererEvent, registry

    class PackageCreateEvent(WhispererEvent):
        serializer_class = PackageSerializer
        event_type = 'package-created'

    registry.register(PackageCreateEvent)

Subscribing to a Whisperer Event
-----------------------------

If ``https://example.com/`` wants to learn when a package created on
``https://your-app.com/``, it can subscribe to ``package-created`` event
like below.

.. code-block:: python

    import requests

    requests.post(
        url='https://your-app.com/whisperer/hooks/',
        headers={
            'Authorization': 'Token <secret-login-token>',
        },
        json={
            'event_type': 'package-created',
            'secret_key': '<secret>',
            'target_url': 'https://example.com/',
            'retry_countdown_config': {
                'choice': 'linear',
                'kwargs': {
                    'base': 1 * 60,
                    'limit': 10 * 60
                }
            }
        }
    )


Delivering an event to subscribed users
---------------------------------------

A whisperer event can be delivered to subscribed users using ``deliver_event`` function

.. code-block:: python

    from django.db.models.signals import post_save
    from whisperer.tasks import deliver_event
    from foo.bar.app.models import Package

    def signal_receiver(instance, created=False, **kwargs):
        if created:
            deliver_event(instance, 'package-created')

    post_save.connect(signal_receiver, Package)


``dj-whisperer`` will inform subscribed users as follows:

.. code-block:: python

    import requests

    requests.post(
        url='https://example.com/',
        headers={
            'Content-Type': 'application/json',
            'X-Whisperer-Event': 'package-created'
        },
        json={
            'event': {
                'type': 'package-created',
                'uuid': 'da81e85139824c6187dd1e58a7d3f971',
            },
            'data': {
                'id': 61,
                'transfer_id': 49,
                'order_number': '248398923123',
                '.....': '......',
            }
        }
    )


Cancelling a subscription
-------------------------
.. code-block:: python

    import requests

    requests.delete(
        url='https://your-app.com/whisperer/hooks/<webhook-id>/',
        headers={
            'Authorization': 'Token <secret-login-token>'
        }
    )

Advanced Usage
==============

Django Whisperer app is highly extensible.

Callback Function
-----------------

When a callback function specified, it can be called after informing
subscribed user with response, event_type, instance and request payload.

.. code-block:: python

    import logging

    logger = logging.getLogger(__name__)

    def callback(response, event_type, instance, payload):
        logger.info('this is a sweety callback function.')
        # some other codes


Subscribing to an event with callback function is as follows:

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
            'callback': 'foo.bar.app.callback',
            'retry_countdown_config': {'choice': 'exponential', 'kwargs': {'base': 2}}
        }
    )

Deliver Event Optional Parameters
---------------------------------

``deliver_event`` function optional parameters:

_async
~~~~~~

default: True

Set ``_async=False`` if you want the code to run sync

.. code-block:: python

    deliver_event(instance, 'package-created', _async=False)

event_uuid
~~~~~~~~~~

default: None

Set ``event_uuid=uuid`` if you want process with spesific WebhookEvent

.. code-block:: python

    deliver_event(
        instance,
        'package-created',
        event_uuid='d960acbe-4193-44b8-b254-df115cf6d2e7'
    )



Settings Paramaters
-------------------

    WHISPERER_REQUEST_TIMEOUT

Default: 10

If you specify a single value for the timeout, like this:

.. code-block:: python

    WHISPERER_REQUEST_TIMEOUT = 5


The timeout value will be applied to both the ``connect`` and the ``read`` timeouts.
Specify a tuple if you would like to set the values separately:

.. code-block:: python

    WHISPERER_REQUEST_TIMEOUT = (5 , 10)

..

    WHISPERER_EVENT_QUEUE_DELAY_SECOND

Default: 360

Specify custom value for how many second before Event Queue objects
register again with trigger_event_queue_events method

.. code-block:: python

    WHISPERER_EVENT_QUEUE_DELAY_SECOND = 720

Custom Retry Countdown
----------------------

When one of ``linear``, ``exponential``, ``fixed`` & ``random`` retry countdown patterns
is not suitable and there is need for custom retry countdown pattern, it can be
possible as below.

.. code-block:: python

    from whisperer.countdown import BaseRetryCountdown, countdown_classes


    @countdown_classes.register(key='custom')
    class CustomRetryCountdown(BaseRetryCountdown):
        def __init__(self, factor):
            self.factor = factor

        def get_value(self, retry_count):
            if retry_count % 2 == 0:
                return 2 * self.factor * retry_count
            return self.factor * retry_count



There must be kwargs serializer class for that countdown

.. code-block:: python

    from rest_framework import serializers
    from whisperer.validators import countdown_kwargs_serializers


    @countdown_kwargs_serializers.register(key='custom')
    class CustomRetryCountdownKwargsSerializer(serializers.Serializer):
        factor = serializers.IntegerField(min_value=1)
Subscribing to an event with this custom retry countdown is as follows:

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
                'choice': 'custom',
                'kwargs': {
                    'factor': 5
                }
            }
        }
    )


Authentication Methods
----------------------

Use can use authentication methods adding auth config on Webhook config field. Only basic authentication supported for now.

For basic authentication:

.. code-block:: python

    import requests

    requests.post(
        url='https://your-app.com/whisperer/hooks/',
        json={
            'event_type': 'order-created',
            'target_url': 'https://example.com/order-created/',
        },
        config={
            'auth': {
                'auth_type': 'basic',
                'username': 'username',
                'password': 'password'
            }
        }
    )

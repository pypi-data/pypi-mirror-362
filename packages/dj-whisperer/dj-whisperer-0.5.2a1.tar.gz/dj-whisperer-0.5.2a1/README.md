# Django Whisperer

[![Build status](https://img.shields.io/bitbucket/pipelines/akinonteam/dj-whisperer)](https://bitbucket.org/akinonteam/dj-whisperer/addon/pipelines/home)
[![Documentation status](https://readthedocs.org/projects/dj-whisperer/badge/?version=latest)](https://dj-whisperer.readthedocs.io/en/latest/?badge=latest)
![PyPI](https://img.shields.io/pypi/v/dj-whisperer)
![PyPI - Django version](https://img.shields.io/pypi/djversions/dj-whisperer)
![PyPI - Python version](https://img.shields.io/pypi/pyversions/dj-whisperer)
![PyPI - License](https://img.shields.io/pypi/l/dj-whisperer)

Whisperer informs subscribed users via an URL when a specific event occurs.

## Installation

Installation using pip:

```
pip install dj-whisperer
```

`whisperer` package has to be added to `INSTALLED_APPS` and `migrate` command has to be run.

```python
INSTALLED_APPS = (
    # other apps here...
    'whisperer',
)
```

## Sample Scenario

Let's give an example using `Package` model. When an event occurs related to a package, subscribed users are gonna be informed. To do so, firstly which events to subscribe must be determined. In order to learn when a package created:

```python
from django.db.models.signals import post_save
from whisperer.events import WhispererEvent, registry
from whisperer.tasks import deliver_event

class PackageCreateEvent(WhispererEvent):
    serializer_class = PackageSerializer
    event_type = 'package-created'

registry.register(PackageCreateEvent)


def signal_receiver(instance, created=False, **kwargs):
    if created:
        deliver_event(instance, 'package-created')

post_save.connect(signal_receiver, Package)
```

When database transaction succeeds, in short when `transaction.on_commit()`, `deliver_event` must be triggered.
Subscribed users now can be informed that a package created if they have created a `Webhook`.

```python
import requests

requests.post(
    url='https://your-app.com/whisperer/hooks/',
    headers={
        'Authorization': 'Token <secret-login-token>',
    },
    json={
        'event_type': 'package-created',
        'secret_key': 'secret',
        'target_url': 'https://example.com/',
    }
)
```

When a package created, `uuid`, `type` & `data` passed through `PackageSerializer` will be posted to https://example.com/.

```python
import requests

requests.post(
    url='https://example.com/',
    headers={
        'Content-Type': 'application/json',
        'X-Whisperer-Event': 'package-created',
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
```

In order to cancel the subscription:

```python
import requests

requests.delete(
    url='https://your-app.com/whisperer/hooks/<webhook-id>/',
    headers={
        'Authorization': 'Token <secret-login-token>',
    }
)
```

To re-trigger events that lost on the queue you must call `whisperer.tasks.trigger_event_queue_events` with scheduler

To automate the removal of outdated event records, schedule the task `whisperer.tasks.delete_outdated_webhook_events` using a scheduler. By default, it targets records older than 12 weeks.

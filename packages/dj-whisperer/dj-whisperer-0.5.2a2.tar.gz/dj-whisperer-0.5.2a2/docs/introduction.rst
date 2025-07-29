Introduction
============

Installation
------------

You can install this package from `PyPI <https://pypi.org/>`_::

    pip install dj-whisperer

You need to append it to the ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'whisperer',
    ]


Then migrate your project::

    python manage.py migrate whisperer


add cron to ``CELERYBEAT_SCHEDULE`` for undelivered event scanner:

.. code-block:: python

    CELERYBEAT_SCHEDULE = {
        ...
        'undelivered-event-scanner-cron': {
            'task': 'whisperer.tasks.undelivered_event_scanner',
            'schedule': get_rand_seconds(60 * 60, deviation_seconds=60 * 30),
            'args': (),
        },
    }




Now you are ready to create your whisperer events, take a look at :doc:`quickstart`.

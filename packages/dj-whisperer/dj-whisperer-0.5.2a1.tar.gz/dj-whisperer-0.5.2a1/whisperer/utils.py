import logging
from datetime import datetime

from celery import current_app
from django.core.cache import cache as django_cache
from django.utils.encoding import force_str
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)


class LockTask(current_app.Task):
    """This abstract class ensures the same tasks run only once at a time"""

    abstract = True

    def __init__(self, *args, **kwargs):
        super(LockTask, self).__init__(*args, **kwargs)
        self.redis_cache = None

    def is_exists_cache_key(self, lock_cache_key):
        if self.redis_cache:
            return True if self.redis_cache.get(lock_cache_key) else False
        else:
            return True if django_cache.get(lock_cache_key) else False

    def get_redis_cache(self):
        if not self.redis_cache:
            try:
                self.redis_cache = get_redis_connection("default")
            except Exception as e:
                logger.info("Unable to connect to Redis. Error: %s" % str(e))
        return self.redis_cache

    def generate_lock_cache_key(self, *args, **kwargs):
        args_key = [force_str(arg) for arg in args]
        kwargs_key = [
            '{}_{}'.format(k, force_str(v)) for k, v in sorted(kwargs.items())
        ]
        return '_'.join([self.name] + args_key + kwargs_key)

    def __call__(self, *args, **kwargs):
        """Check task"""
        lock_cache_key = self.generate_lock_cache_key(*args, **kwargs)
        self.redis_cache = self.get_redis_cache()

        if not self.is_exists_cache_key(lock_cache_key):
            lock_time = datetime.now().isoformat()
            if self.redis_cache:
                self.redis_cache.set(
                    lock_cache_key, lock_time, 2 ** self.request.retries
                )
            else:
                django_cache.set(
                    lock_cache_key, lock_time, timeout=2 ** self.request.retries
                )
            try:
                return self.run(*args, **kwargs)
            finally:
                if self.redis_cache:
                    self.redis_cache.delete(lock_cache_key)
                else:
                    django_cache.delete(lock_cache_key)
        else:
            logger.info("Task %s is already running.." % self.name)


class Registry(object):
    def __init__(self):
        self._registry = {}

    def __contains__(self, key):
        return key in self._registry

    def __getitem__(self, key):
        return self._registry[key]

    def register(self, key):
        def decorator(cls):
            self._registry[key] = cls
            return cls

        return decorator


class Slices(object):
    def __init__(self, iterable, size):
        self.iterable = iterable
        self.size = size
        self.offset = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            data_slice = self.iterable[
                self.offset * self.size : (self.offset + 1) * self.size
            ]
            self.offset += 1
            if not len(data_slice):
                raise StopIteration()
            return data_slice
        except IndexError:
            raise StopIteration()

    def next(self):
        # TODO: If python 2.7 support dropped remove this method
        data_slice = self.iterable[
            self.offset * self.size : (self.offset + 1) * self.size
        ]
        self.offset += 1
        if not data_slice:
            raise StopIteration
        return data_slice

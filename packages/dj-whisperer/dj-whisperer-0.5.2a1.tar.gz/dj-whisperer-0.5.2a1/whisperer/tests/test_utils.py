from django.core.cache import cache as django_cache
from django.test import TestCase, override_settings
from django_redis import get_redis_connection
from mock import Mock, patch

from whisperer.utils import LockTask


class LockTaskTests(TestCase):

    redis_connection = get_redis_connection("default")

    class TestLockTask(LockTask):
        abstract = True
        name = 'test_lock_task'
        request = Mock(retries=3)

        def run(self, *args, **kwargs):
            # This is a test task that does nothing
            pass

    def tearDown(self):
        self.redis_connection.flushall()

    def test_lock_task_runs_with_redis_caching(self):
        # Test when Redis is available
        test_lock_task = self.TestLockTask()

        with patch.object(test_lock_task, 'run') as mock_run:
            test_lock_task.__call__("test_arg1", key2="test_arg2")
            mock_run.assert_called_once()

    def test_lock_task_not_run_with_redis_caching(self):
        # Test when Redis is available
        test_lock_task = self.TestLockTask()
        lock_cache_key = test_lock_task.generate_lock_cache_key(
            "test_arg1", key2="test_arg2"
        )
        self.redis_connection.set(lock_cache_key, "value")

        with patch.object(test_lock_task, 'run') as mock_run:
            test_lock_task.__call__("test_arg1", key2="test_arg2")
            mock_run.assert_not_called()

    @override_settings(
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            }
        }
    )
    def test_lock_task_runs_with_django_caching(self):
        # Test when Redis unavailable
        test_lock_task = self.TestLockTask()
        django_cache.clear()

        with patch.object(test_lock_task, 'run') as mock_run:
            test_lock_task.__call__("test_arg1", key2="test_arg2")
            mock_run.assert_called_once()

    @override_settings(
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            }
        }
    )
    def test_lock_task_not_run_with_django_caching(self):
        # Test when Redis unavailable
        test_lock_task = self.TestLockTask()
        lock_cache_key = test_lock_task.generate_lock_cache_key(
            "test_arg1", key2="test_arg2"
        )
        django_cache.set(lock_cache_key, "value")

        with patch.object(test_lock_task, 'run') as mock_run:
            test_lock_task.__call__("test_arg1", key2="test_arg2")
            mock_run.assert_not_called()

import random

from whisperer.utils import Registry

countdown_classes = Registry()


class BaseRetryCountdown(object):
    def get_value(self, retry_count):
        raise NotImplementedError

    def __repr__(self):
        attrs = ['%s: %s' % (k, v) for k, v in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))


@countdown_classes.register(key='fixed')
class FixedRetryCountdown(BaseRetryCountdown):
    def __init__(self, seconds):
        super(FixedRetryCountdown, self).__init__()
        self.seconds = seconds

    def get_value(self, retry_count):
        return self.seconds


@countdown_classes.register(key='linear')
class LinearRetryCountdown(BaseRetryCountdown):
    def __init__(self, base, limit=None):
        super(LinearRetryCountdown, self).__init__()
        self.base = base
        self.limit = limit

    def get_value(self, retry_count):
        count = self.base * retry_count
        if self.limit is None:
            return count
        return min(count, self.limit)


@countdown_classes.register(key='exponential')
class ExponentialRetryCountdown(BaseRetryCountdown):
    def __init__(self, base, factor=1, limit=None):
        super(ExponentialRetryCountdown, self).__init__()
        self.base = base
        self.limit = limit
        self.factor = factor

    def get_value(self, retry_count):
        count = (self.base ** retry_count) * self.factor
        if self.limit is None:
            return count
        return min(count, self.limit)


@countdown_classes.register(key='random')
class RandomRetryCountdown(BaseRetryCountdown):
    def __init__(self, min_value, max_value):
        super(RandomRetryCountdown, self).__init__()
        self.min_value = min_value
        self.max_value = max_value

    def get_value(self, retry_count):
        return random.randint(self.min_value, self.max_value)

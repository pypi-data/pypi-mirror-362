import django

if django.VERSION >= (2, 0, 0):
    from django.utils.encoding import smart_str as smart
else:
    from django.utils.encoding import smart_text as smart

from whisperer import codes


class BaseException(Exception):
    code = codes.undefined

    def __init__(self, *args, **kwargs):
        if not isinstance(self.code, dict):
            raise Exception('parameter type must be a dict')
        code = self.code.get('code', 'undefined')
        message = getattr(self.codes, '%s' % code)
        self.message = message.get('en')
        self.obj = kwargs.get('obj', None)
        self.target = kwargs.get('target', None)
        self.params = kwargs.get('params')
        if self.params and isinstance(self.params, dict):
            self.message = smart(self.message).format(**self.params)
        elif self.params and isinstance(self.params, (list, set, tuple)):
            self.message = smart(self.message).format(*self.params)

        Exception.__init__(self, smart("{0}:{1}").format(code, self.message))

    def __new__(cls, *args, **kwargs):
        obj = super(BaseException, cls).__new__(cls)
        obj.__init__(*args, **kwargs)
        try:
            getattr(cls.codes, '%s' % obj.code.get('code'))
        except AttributeError:
            pass
        return obj

    @property
    def codes(self):
        return codes


class WebhookDoesNotExist(BaseException):
    code = codes.webhook_100_1


class WebhookAlreadyRegistered(BaseException):
    code = codes.webhook_100_2


class WebhookEventDoesNotExist(BaseException):
    code = codes.event_100_1


class EventAlreadyDelivered(BaseException):
    code = codes.event_100_3


class UnknownEventType(BaseException):
    code = codes.event_100_2


class ImproperlyConfigured(BaseException):
    code = codes.event_100_4


class AlreadyRegisteredEvent(BaseException):
    code = codes.event_100_5


class EventStillInProgress(BaseException):
    code = codes.event_100_6

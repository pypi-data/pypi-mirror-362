from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from whisperer.utils import Registry

countdown_kwargs_serializers = Registry()


@countdown_kwargs_serializers.register(key='fixed')
class FixedRetryCountdownKwargsSerializer(serializers.Serializer):
    seconds = serializers.IntegerField(min_value=0, write_only=True)


@countdown_kwargs_serializers.register(key='linear')
class LinearRetryCountdownKwargsSerializer(serializers.Serializer):
    base = serializers.IntegerField(min_value=0, write_only=True)
    limit = serializers.IntegerField(
        min_value=0, required=False, allow_null=True, write_only=True
    )


@countdown_kwargs_serializers.register(key='exponential')
class ExponentialRetryCountdownKwargsSerializer(serializers.Serializer):
    base = serializers.IntegerField(min_value=0, write_only=True)
    factor = serializers.IntegerField(min_value=1, default=1, required=False)
    limit = serializers.IntegerField(
        min_value=0, required=False, allow_null=True, write_only=True
    )


@countdown_kwargs_serializers.register(key='random')
class RandomRetryCountdownKwargsSerializer(serializers.Serializer):
    min_value = serializers.IntegerField(min_value=0, write_only=True)
    max_value = serializers.IntegerField(min_value=0, write_only=True)

    def validate(self, attrs):
        attrs = super(RandomRetryCountdownKwargsSerializer, self).validate(attrs)
        if attrs['min_value'] >= attrs['max_value']:
            raise ValidationError("'max_value' must be greater than 'min_value'.")
        return attrs

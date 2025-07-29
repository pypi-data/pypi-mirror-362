from rest_framework import serializers

from whisperer.tests.models import Foo, Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class FooSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foo
        fields = '__all__'

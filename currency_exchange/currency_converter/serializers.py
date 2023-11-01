from rest_framework import serializers
from .models import Currency, ExchangeRate


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('code', 'name')


class CustomFormattedDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        return value.strftime('%d-%m-%Y %H:%M')


class ExchangeRateSerializer(serializers.ModelSerializer):
    datetime = CustomFormattedDateTimeField()

    class Meta:
        model = ExchangeRate
        fields = ('rate', 'datetime')

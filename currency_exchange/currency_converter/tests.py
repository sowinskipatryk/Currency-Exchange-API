from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from currency_converter.models import Currency, ExchangeRate


class CurrencyExchangeAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Currency.objects.create(code="EUR", name="Euro")
        Currency.objects.create(code="USD", name="US Dollar")

        ExchangeRate.objects.create(from_currency=Currency.objects.get(code="EUR"),
                                    to_currency=Currency.objects.get(code="USD"),
                                    rate='1.0600')

    def test_list_available_currencies(self):
        response = self.client.get('/currency/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_order_by_name_descending(self):
        currencies = Currency.objects.all().order_by('-name')
        self.assertEqual(currencies[0].code, "USD")

    def test_filter_by_currency_code(self):
        response = self.client.get('/currency/?code=USD')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['code'], 'USD')
        self.assertEqual(len(response.data), 1)

    def test_filter_by_partial_name(self):
        response = self.client.get('/currency/?name=dollar')

        self.assertEqual(response.status_code, 200)
        filtered_currencies = [currency['name'] for currency in response.data]
        self.assertIn("US Dollar", filtered_currencies)
        self.assertEqual(len(response.data), 1)

    def test_get_exchange_rate(self):
        response = self.client.get('/currency/EUR/USD/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rate'], '1.0600')

    def test_get_exchange_rate_nonexistent_pair(self):
        response = self.client.get('/currency/GBP/JPY/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_exchange_rate_invalid_currency(self):
        response = self.client.get('/currency/EUR/INVALID/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

from django.core.management.base import BaseCommand
from currency_converter.models import Currency, ExchangeRate
import yfinance as yf


class Command(BaseCommand):
    help = 'Fetch and save exchange rates'

    def handle(self, *args, **options):
        currencies = [{'code': 'PLN', 'name': 'Polish Zloty'},
                      {'code': 'USD', 'name': 'US Dollar'},
                      {'code': 'EUR', 'name': 'Euro'},
                      {'code': 'GBP', 'name': 'British Pound'},
                      {'code': 'JPY', 'name': 'Japanese Yen'}]

        for from_currency_dict in currencies:
            for to_currency_dict in currencies:
                if from_currency_dict['code'] != to_currency_dict['code']:
                    from_currency, created = Currency.objects.get_or_create(code=from_currency_dict['code'],
                                                                            name=from_currency_dict['name'])
                    to_currency, created = Currency.objects.get_or_create(code=to_currency_dict['code'],
                                                                          name=to_currency_dict['name'])

                    ticker = f"{from_currency_dict['code']}{to_currency_dict['code']}=X"
                    exchange_data = yf.Ticker(ticker)
                    rate = exchange_data.history(period="1d")["Close"].values[0]

                    exchange_rate, created = ExchangeRate.objects.update_or_create(
                        from_currency=from_currency,
                        to_currency=to_currency,
                        defaults={"rate": rate}
                    )

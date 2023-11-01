from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.code})"


class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='from_rates')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='to_rates')
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_currency.code}{self.to_currency.code} @ {self.rate} [{self.datetime.strftime('%d-%m-%Y %H:%M:%S')}]"

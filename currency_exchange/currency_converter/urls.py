from django.urls import path
from .views import CurrencyList, ExchangeRateRetrieve

urlpatterns = [
    path('', CurrencyList.as_view(), name='currency-list'),
    path('<str:from_currency>/<str:to_currency>/', ExchangeRateRetrieve.as_view(), name='exchange-rate-retrieve'),
]

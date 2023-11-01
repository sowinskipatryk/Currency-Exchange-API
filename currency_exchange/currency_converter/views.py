from datetime import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Currency, ExchangeRate
from .serializers import CurrencySerializer, ExchangeRateSerializer


class CurrencyList(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        code = self.request.query_params.get('code', None)
        name = self.request.query_params.get('name', None)
        ordering = self.request.query_params.get('ordering', None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        if code is not None:
            queryset = queryset.filter(code__icontains=code)

        if ordering is not None:
            queryset = queryset.order_by(ordering)

        return queryset


class ExchangeRateRetrieve(generics.RetrieveAPIView):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer

    def retrieve(self, request, *args, **kwargs):
        from_currency = self.kwargs.get('from_currency')
        to_currency = self.kwargs.get('to_currency')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        # Check if the currency pair is invalid
        if not ExchangeRate.objects.filter(from_currency__code=from_currency, to_currency__code=to_currency).exists():
            response_data = {
                'error': f"{from_currency}/{to_currency} currency pair does not exist in the database"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%d-%m-%Y')
            end_date = datetime.strptime(end_date, '%d-%m-%Y')
            queryset = ExchangeRate.objects.filter(
                from_currency__code=from_currency,
                to_currency__code=to_currency,
                datetime__range=(start_date, end_date)
            )
        elif start_date:
            start_date = datetime.strptime(start_date, '%d-%m-%Y')
            queryset = ExchangeRate.objects.filter(
                from_currency__code=from_currency,
                to_currency__code=to_currency,
                datetime__gte=start_date
            )

        elif end_date:
            end_date = datetime.strptime(end_date, '%d-%m-%Y')
            queryset = ExchangeRate.objects.filter(
                from_currency__code=from_currency,
                to_currency__code=to_currency,
                datetime__lte=end_date
            )
        else:
            queryset = ExchangeRate.objects.filter(
                from_currency__code=from_currency,
                to_currency__code=to_currency)

        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            response_data = {
                'message': 'No results found for the given date range'
            }
            return Response(response_data, status=status.HTTP_200_OK)

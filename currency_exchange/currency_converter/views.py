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
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        ordering = self.request.query_params.get('ordering', None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        if code is not None:
            queryset = queryset.filter(code__icontains=code)

        if ordering is not None:
            queryset = queryset.order_by(ordering)

        if datetime is not None:
            queryset = queryset.filter(datetime__range=[date_from, date_to])

        return queryset


class ExchangeRateRetrieve(generics.RetrieveAPIView):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer

    def get_object(self):
        from_currency = self.kwargs.get('from_currency')
        to_currency = self.kwargs.get('to_currency')

        try:
            return self.queryset.get(from_currency__code=from_currency, to_currency__code=to_currency)
        except ExchangeRate.DoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            response_data = {
                'error': f"{self.kwargs['from_currency']}/{self.kwargs['to_currency']} currency pair does not exist in the database"}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

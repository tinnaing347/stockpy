from django_filters import rest_framework as filters
from .models import Symbol, DailyStock

class SymbolFilter(filters.FilterSet):
    class Meta:
        model = Symbol
        fields = ['symbol']

class DailyStockFilter(filters.FilterSet):
    start_date = filters.DateTimeFilter(field_name='date', lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name='date', lookup_expr='lt')

    class Meta:
        model = DailyStock
        fields = ['date', 'symbol']
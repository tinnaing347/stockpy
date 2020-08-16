from django_filters import rest_framework as filters
from .models import Symbol, RealTimeStock, DailyStock

class SymbolFilter(filters.FilterSet):
    class Meta:
        model = Symbol
        fields = ['symbol']

class RealTimeStockFilter(filters.FilterSet):
    start_date_time = filters.DateTimeFilter(field_name='date_time', lookup_expr='gte')
    end_date_time = filters.DateTimeFilter(field_name='date_time', lookup_expr='lt')

    class Meta:
        model = RealTimeStock
        fields = ['date_time', 'symbol']

class DailyStockFilter(filters.FilterSet):
    start_date = filters.DateTimeFilter(field_name='date', lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name='date', lookup_expr='lt')

    class Meta:
        model = DailyStock
        fields = ['date', 'symbol']
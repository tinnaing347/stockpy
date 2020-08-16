from django.shortcuts import render
from .serializers import SymbolSerializer, RealTimeStockSerializer, DailyStockSerializer
from .models import Symbol, RealTimeStock, DailyStock
from rest_framework import generics, views, reverse, response, viewsets
from .filters import SymbolFilter, RealTimeStockFilter, DailyStockFilter
from stockpy.paginators import StandardResultPagination, LargeResultPagination
# Create your views here.

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


class StocksRootView(views.APIView):
    """ Root view allows user to browse API via hyperlinks
    """
    def get(self, request, format=None):
        routes = {
            'symbol': reverse.reverse('stocks:symbol-list', request=request, format=format),
            'real-time-stock': reverse.reverse('stocks:real-time-stock-list', request=request, format=format),
            'daily-stock': reverse.reverse('stocks:daily-stock-list', request=request, format=format)
        }
        return response.Response(routes)


class CachingListView(generics.ListAPIView):
    """ Caches the list views for 30 minutes
    """
    @method_decorator(cache_page(60 * 30)) 
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class SymbolListView(CachingListView):
    queryset = Symbol.objects.all().order_by('symbol')
    serializer_class = SymbolSerializer
    filter_class = SymbolFilter
    pagination_class = StandardResultPagination

class RealTimeStockListView(CachingListView):
    queryset = RealTimeStock.objects.all().order_by('symbol','date_time')
    serializer_class = RealTimeStockSerializer
    filter_class = RealTimeStockFilter
    pagination_class = LargeResultPagination

class DailyStockListView(CachingListView):
    queryset = DailyStock.objects.all().order_by('symbol','date')
    serializer_class = DailyStockSerializer
    filter_class = DailyStockFilter
    pagination_class = LargeResultPagination
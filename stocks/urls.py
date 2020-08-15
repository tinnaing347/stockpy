from django.urls import include, path
from rest_framework import routers
from . import views

app_name = 'stocks'

urlpatterns = [
    path('', views.StocksRootView.as_view(), name='stocks-root'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('symbol/', views.SymbolListView.as_view(), name='symbol-list'),
    path('daily-stock/', views.DailyStockListView.as_view(), name='daily-stock-list'),
]
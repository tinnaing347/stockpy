from rest_framework import serializers
from .models import Symbol, DailyStock

class SymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = '__all__'


class DailyStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyStock
        fields = '__all__'